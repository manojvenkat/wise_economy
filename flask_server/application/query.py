from datetime import datetime

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import text, func

from application.models import TrackingRecord, name_to_column_dict


class TrackingRecordObject(SQLAlchemyObjectType):
    class Meta:
        model = TrackingRecord
        interfaces = (relay.Node, )


class Dictionary(graphene.ObjectType):
    key = graphene.String()
    value = graphene.String()


class GenericDataField(graphene.ObjectType):
    column = graphene.List(Dictionary)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    analyze_tracking_records = graphene.List(
        GenericDataField,
        group_by=graphene.List(graphene.String),
        order_by=graphene.List(graphene.String),
        sum_of=graphene.List(graphene.String),
        from_time=graphene.String(),
        to_time=graphene.String(),
        ratio_of=graphene.List(graphene.String),
        filter_by=graphene.List(graphene.String),
    )

    def resolve_analyze_tracking_records(self, info, **kwargs):
        data_entries = _generic_query_runner(kwargs)
        group_by_columns = kwargs.get("group_by", [])
        sum_columns = kwargs.get("sum_of", [])
        ratio_columns = kwargs.get("ratio_of", [])
        return [
            get_entry_for_output_json(
                data_entry,
                group_by_columns,
                sum_columns,
                ratio_columns,
            )
            for data_entry in data_entries
        ]


def get_entry_for_output_json(data_entry, group_by_columns, sum_columns, ratio_columns):
    _list = []

    if len(ratio_columns) > 0:
        for i in range(len(ratio_columns)):
            _list.append(Dictionary(ratio_columns[i].replace(':', '_by_'), data_entry[i]))

    data_entry = data_entry[len(ratio_columns):]
    if len(sum_columns) > 0:
        for i in range(len(sum_columns)):
            _list.append(Dictionary(sum_columns[i] + "_sum", data_entry[i]))

    data_entry = data_entry[len(sum_columns):]
    if len(group_by_columns) > 0:
        for i in range(len(group_by_columns)):
            _list.append(Dictionary(group_by_columns[i], data_entry[i]))

    return GenericDataField(column=_list)


def _generic_query_runner(kwargs):
    from_time, to_time = _extract_time_filtering_args(kwargs)
    group_by_columns = _get_grouping_columns(kwargs)
    order_by_columns = _get_ordering_columns(kwargs)
    sum_columns = _get_summing_columns(kwargs)
    ratio_columns = _get_ratio_columns(kwargs)
    filter_columns = _get_filtering_columns(kwargs)
    data_entries = _run_query(
        from_time=from_time,
        to_time=to_time,
        group_by_columns=group_by_columns,
        order_by_columns=order_by_columns,
        sum_columns=sum_columns,
        ratio_columns=ratio_columns,
        filter_columns=filter_columns,
    )
    return data_entries


def _extract_time_filtering_args(kwargs):
    try:
        from_time = datetime.strptime(kwargs.get("from_time"), "%Y-%m-%d")
    except ValueError:
        from_time = datetime(1970, 1, 1)
    try:
        to_time = datetime.strptime(kwargs.get("to_time"), "%Y-%m-%d")
    except ValueError:
        to_time = datetime.now()
    return from_time, to_time


def _run_query(from_time, group_by_columns, order_by_columns, sum_columns, to_time, ratio_columns, filter_columns):
    return TrackingRecord.query \
        .filter(text(filter_columns)) \
        .filter(TrackingRecord.date <= to_time) \
        .filter(TrackingRecord.date >= from_time) \
        .with_entities(
            *ratio_columns,
            *sum_columns,
            *group_by_columns, ) \
        .group_by(*group_by_columns) \
        .order_by(text(order_by_columns)) \
        .all()


def _get_grouping_columns(kwargs):
    group_by = kwargs.get("group_by", [])
    return [
        name_to_column_dict()[column_name]
        for column_name in group_by
    ]


def _get_summing_columns(kwargs):
    sum_of = kwargs.get("sum_of", [])
    return [
        func.sum(name_to_column_dict()[column_name]).label(column_name + '_sum')
        for column_name in sum_of
    ]


def _get_ratio_columns(kwargs):
    ratio_of = kwargs.get("ratio_of", [])
    ratios = []
    for ratio in ratio_of:
        ratio_columns = [name_to_column_dict()[column_name] for column_name in ratio.split(':')]
        ratios.append((ratio_columns[0]/ratio_columns[1]).label(ratio.replace(':', '_by_')))
    return ratios


def _get_ordering_columns(kwargs):
    order_by = kwargs.get("order_by", [])
    order_by_columns = ""
    for ordering_clause in order_by:
        order_by_columns += ordering_clause
    return order_by_columns


def _get_filtering_columns(kwargs):
    filter_by = kwargs.get("filter_by", [])
    filter_query_string = ""
    if len(filter_by) > 0:
        for filtering_clause in filter_by:
            filter_query_string += filtering_clause + " and "
        filter_query_string = filter_query_string[:len(filter_query_string)-4]
    return filter_query_string
