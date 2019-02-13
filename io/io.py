# coding: utf-8

# Author: Moju Wu
#
# IO for relation.json

import json
from structure import relationStructure


def load_relation(json_file):
    relation = []
    with open(json_file) as f:
        relation_dict_list = json.load(f)
        for relation_dict in relation_dict_list:
            relation_type = relation_dict["relationType"]
            arg1 = relation_dict["mentionArg1"]
            arg2 = relation_dict["mentionArg2"]

    return relation


def load_entity_dict_from_files():
    return


def load_relation_from_files(json_files, val_portion=0.0):
    """
    Load relation and argument1 and argument2 from multiple json files.

    :param json_files: list of input json files
    :param val_portion: a portion of the data to reserve for validation
    :return: a tuple of the data and validation data
    """
    data = []
    for json_file in json_files:
        with open(json_file) as f:
            data = data + load_relation(f)
    print("Loaded data size:", len(data))

    val_data = []
    if val_portion > 0.0:
        val_size = int(len(data) * val_portion)
        rest_size = len(data) - val_size
        val_data = data[rest_size:]
        data = data[:rest_size]
        print("Training and dev set sizes:", (len(data), len(val_data)))

    return data, val_data


def load_relation_graphs_from_files(json_files, val_portion=0.0, load_vertices=True):
    """
    Load semantic graphs from multiple json files and if specified reserve a portion of the data for validation.

    :param json_files: list of input json files
    :param val_portion: a portion of the data to reserve for validation
    :return: a tuple of the data and validation data
    """
    data = []
    for json_file in json_files:
        with open(json_file) as f:
            if load_vertices:
                data = data + json.load(f)
            else:
                data = data + json.load(f, object_hook=dict_to_graph_with_no_vertices)
    print("Loaded data size:", len(data))

    val_data = []
    if val_portion > 0.0:
        val_size = int(len(data)*val_portion)
        rest_size = len(data) - val_size
        val_data = data[rest_size:]
        data = data[:rest_size]
        print("Training and dev set sizes:", (len(data), len(val_data)))
    return data, val_data


def load_relation_graphs_from_file(json_file, val_portion=0.0, load_vertices=True):
    """
    Load semantic graphs from a json file and if specified reserve a portion of the data for validation.

    :param json_file: the input json file
    :param val_portion: a portion of the data to reserve for validation
    :return: a tuple of the data and validation data
    """
    return load_relation_graphs_from_files([json_file], val_portion, load_vertices)


def dict_to_graph_with_no_vertices(d):
    if 'vertexSet' in d:
        del d['vertexSet']
    return d
