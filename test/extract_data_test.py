from components.extract_data import nodes_text_to_list_of_dict, relationships_text_to_list_of_dict, \
    get_nodes_relationships_from_rawtext, duplicate_nodes_relationships
import unittest


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


class TestDuplicateNodesRelationships(unittest.TestCase):
    def setUp(self):
        self.duplicate_nodes_relationships = duplicate_nodes_relationships  # replace with actual function name

    def test_duplicate_nodes(self):
        data = {
            "nodes": [
                {
                    "name": "浩瀚科技",
                    "label": "公司",
                    "properties": {
                        "名称": "浩瀚科技"
                    }
                },
                {
                    "name": "浩瀚科技",
                    "label": "公司",
                    "properties": {
                        "地址": "北京"
                    }
                }
            ],
            "relationships": []
        }
        result = self.duplicate_nodes_relationships(data)
        self.assertEqual(len(result['nodes']), 1)
        self.assertEqual(result['nodes'][0]['properties'], {"名称": "浩瀚科技", "地址": "北京"})

    def test_duplicate_relationships(self):
        data = {
            "nodes": [],
            "relationships": [
                {
                    "start": "浩瀚科技",
                    "end": "李伟",
                    "type": "总裁",
                    "properties": {"开始时间": "2020"}
                },
                {
                    "start": "浩瀚科技",
                    "end": "李伟",
                    "type": "总裁",
                    "properties": {"结束时间": "2025"}
                }
            ]
        }
        result = self.duplicate_nodes_relationships(data)
        self.assertEqual(len(result['relationships']), 1)
        self.assertEqual(result['relationships'][0]['properties'], {"开始时间": "2020", "结束时间": "2025"})


if __name__ == '__main__':
    unittest.main()
