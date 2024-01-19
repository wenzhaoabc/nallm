import unittest
import json
import sys
import os

sys.path.insert(0, "/Users/I745173/Documents/workspace/projects/nallm/nallm")


from components.extract_data import (
    nodes_text_to_list_of_dict,
    relationships_text_to_list_of_dict,
    get_nodes_relationships_from_rawtext,
    duplicate_nodes_relationships,
)


def extract_nodes_test():
    data = """
- ["李薇", "人", {"年龄":25, "职业":"律师", "姓名":"李薇"}]
- ["Bob", "人", {"职业":"记者","姓名":"Bob"}]
- ["liwei.com", "网站", {"网址": "www.liwei.com"}]
- ["bob.com", "网站", {"网址": "www.bob.com"}]
    """

    nodes = nodes_text_to_list_of_dict(data)
    for node in nodes:
        print(node)


def extract_relationship_test():
    data = """
- ["李薇", "室友", "Bob", {"开始时间":2021}]
- ["李薇", "拥有", "liwei.com", {}]
- ["Bob", "拥有", "bob.com", {})]
    """
    relationships = relationships_text_to_list_of_dict(data)
    for relationship in relationships:
        print(relationship)


def get_nodes_relationships_test():
    data = """
文本数据:李薇是律师，今年25岁，Bob从2001年起就是她的室友。Bob是一名记者。李薇拥有网页www.liwei.com, Bob拥有网页www.bob.com。
Nodes:
- ["李薇", "人", {"年龄":25, "职业":"律师"、"姓名":"李薇"}]
- ["Bob", "人", {"职业":"记者","姓名":"Bob"}]
- ["liwei.com", "网站", {"网址": "www.liwei.com"}]
- ["bob.com", "网站", {"网址": "www.bob.com"}]
Relationships:
- ["李薇", "室友", "Bob", {"开始时间":2021}]
- ["李薇", "拥有", "liwei.com", {}]
- ["Bob", "拥有", "bob.com", {})]
    """
    res = get_nodes_relationships_from_rawtext(data)
    print(res["nodes"])
    print(res["relationships"])


# extract_nodes_test()
# print("==============")
# extract_relationship_test()
# print("===============")
# get_nodes_relationships_test()


def test_duplicate_nodes_relationships():
    jsonData = """
{"nodes": [{"name": "HaohanTech", "label": "Company", "properties": {"name": "浩瀚科技"}}, {"name": "LiWei", "label": "Person", "properties": {"job": "总裁", "name": "李伟"}}, {"name": "ZhangTing", "label": "Person", "properties": {"job": "研发部部长", "name": "张婷"}}, {"name": "HanMei", "label": "Person", "properties": {"job": "市场部部长", "name": "韩梅"}}, {"name": "ZhaoQiang", "label": "Person", "properties": {"job": "人事部部长", "name": "赵强"}}, {"name": "SunHao", "label": "Person", "properties": {"job": "财务部部长", "name": "孙浩"}}, {"name": "XingyunBrowser", "label": "Product", "properties": {"name": "星云浏览器"}}, {"name": "Huawei", "label": "Company", "properties": {"name": "华为"}}, {"name": "Xiaomi", "label": "Company", "properties": {"name": "小米"}}, {"name": "OPPO", "label": "Company", "properties": {"name": "OPPO"}}, {"name": "JingdongMall", "label": "Company", "properties": {"name": "京东商城"}}], "relationships": [{"start": "HaohanTech", "end": "LiWei", "type": "led_by", "properties": {}}, {"start": "HaohanTech", "end": "ZhangTing", "type": "has_department_head", "properties": {"department": "研发部"}}, {"start": "HaohanTech", "end": "HanMei", "type": "has_department_head", "properties": {"department": "市场部"}}, {"start": "HaohanTech", "end": "ZhaoQiang", "type": "has_department_head", "properties": {"department": "人事部"}}, {"start": "HaohanTech", "end": "SunHao", "type": "has_department_head", "properties": {"department": "财务部"}}, {"start": "HaohanTech", "end": "XingyunBrowser", "type": "produces", "properties": {}}, {"start": "Huawei", "end": "XingyunBrowser", "type": "uses", "properties": {}}, {"start": "Xiaomi", "end": "XingyunBrowser", "type": "uses", "properties": {}}, {"start": "OPPO", "end": "XingyunBrowser", "type": "uses", "properties": {}}, {"start": "HaohanTech", "end": "JingdongMall", "type": "cooperates_with", "properties": {}}, {"start": "LiWei", "end": "ZhangTing", "type": "communicates_with", "properties": {}}, {"start": "LiWei", "end": "HanMei", "type": "communicates_with", "properties": {}}, {"start": "LiWei", "end": "ZhaoQiang", "type": "communicates_with", "properties": {}}, {"start": "LiWei", "end": "SunHao", "type": "communicates_with", "properties": {}}]}
"""
    dictData = json.loads(jsonData)
    res = duplicate_nodes_relationships(dictData)
    for node in res["nodes"]:
        print(node)
    for rela in res["relationships"]:
        print(rela)


test_duplicate_nodes_relationships()
