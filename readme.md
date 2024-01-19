# graph database with llm

## test case 1

prompts

```text
你是一名数据科学家，在一家正在构建图形数据库的公司工作。您的任务是从文本数据中提取信息并将其转换为图形数据库中适用的格式。
请以[ENTITY_ID, TYPE, PROPERTIES]的形式提取一组节点，并以[ENTITY_ID_1, RELATIONSHIP, ENTITY_ID_2, PROPERTIES]的形式提取一组关系。
需要注意，ENTITY_ID_1和ENTITY_ID_2应当具有匹配ENTITY_ID的节点存在。如果你不能将一个关系与一对节点配对，那就不要添加它。
当您找到想要添加的节点或关系时，请尝试为其创建描述实体的抽象TYPE，您也可以将其视为标签。请直接输出您提取出的节点和关系，不要输出任何分析过程。

例子:
文本数据:李薇是律师，今年25岁，Bob从2001年起就是她的室友。Bob是一名记者。李薇拥有网页www.liwei.com, Bob拥有网页www.bob.com。
Nodes:
- ["李薇", "人", {"年龄":25, "职业":"律师"、"姓名":"李薇"}]
- ["Bob", "人", {"职业":"记者","姓名":"Bob"}]
- ["liwei.com", "网站", {"网址": "www.liwei.com"}]
- ["bob.com", "网站", {"网址": "www.bob.com"}]
Relationships:
- ["李薇", "室友", "Bob", {"开始时间":2021}]
- ["李薇", "拥有", "liwei.com", {}]
- ["Bob", "拥有", "bob.com", {}]
```

input [test.txt](./static/test.txt) language = zh
http://wenzhaoabc.com:7474
output

```text
Nodes:
- ["浩瀚科技", "公司", {"名称": "浩瀚科技"}]
- ["李伟", "人", {"姓名": "李伟", "职位": "总裁"}]
- ["张婷", "人", {"姓名": "张婷", "职位": "研发部部长"}]
- ["韩梅", "人", {"姓名": "韩梅", "职位": "市场部部长"}]
- ["赵强", "人", {"姓名": "赵强", "职位": "人事部部长"}]
- ["孙浩", "人", {"姓名": "孙浩", "职位": "财务部部长"}]
- ["王磊", "人", {"姓名": "王磊", "职位": "算法组组长"}]
- ["李远", "人", {"姓名": "李远", "职位": "资深工程师"}]
- ["徐晓明", "人", {"姓名": "徐晓明", "职位": "资深工程师"}]
- ["陈燕", "人", {"姓名": "陈燕", "职位": "软件开发组组长"}]
- ["刘颖", "人", {"姓名": "刘颖"}]
- ["黄志强", "人", {"姓名": "黄志强"}]
- ["周杰", "人", {"姓名": "周杰", "职位": "人工智能小组组长"}]
- ["张华", "人", {"姓名": "张华", "职位": "资深研究员"}]
- ["李思", "人", {"姓名": "李思", "职位": "工程师"}]
- ["王晓丽", "人", {"姓名": "王晓丽", "职位": "市场策划师"}]
- ["林涛", "人", {"姓名": "林涛", "职位": "数据分析师"}]
- ["刘倩", "人", {"姓名": "刘倩", "职位": "客户经理"}]
- ["赵天宇", "人", {"姓名": "赵天宇", "职位": "媒介专员"}]
- ["徐杰", "人", {"姓名": "徐杰", "职位": "网络营销师"}]
- ["孙玲", "人", {"姓名": "孙玲", "职位": "招聘专员"}]
- ["马超", "人", {"姓名": "马超", "职位": "员工关系主管"}]
- ["杜慧", "人", {"姓名": "杜慧", "职位": "会计师"}]
- ["周雷", "人", {"姓名": "周雷", "职位": "财务分析师"}]
- ["星云浏览器", "产品", {"名称": "星云浏览器"}]
- ["华为", "公司", {"名称": "华为"}]
- ["小米", "公司", {"名称": "小米"}]
- ["OPPO", "公司", {"名称": "OPPO"}]
- ["京东商城", "公司", {"名称": "京东商城"}]

Relationships:
- ["浩瀚科技", "总裁", "李伟", {}]
- ["浩瀚科技", "部门", "研发部", {}]
- ["浩瀚科技", "部门", "市场部", {}]
- ["浩瀚科技", "部门", "人事部", {}]
- ["浩瀚科技", "部门", "财务部", {}]
- ["研发部", "部门长", "张婷", {}]
- ["市场部", "部门长", "韩梅", {}]
- ["人事部", "部门长", "赵强", {}]
- ["财务部", "部门长", "孙浩", {}]
- ["研发部", "小组", "算法组", {}]
- ["研发部", "小组", "软件开发组", {}]
- ["研发部", "小组", "人工智能小组", {}]
- ["算法组", "组长", "王磊", {}]
- ["软件开发组", "组长", "陈燕", {}]
- ["人工智能小组", "组长", "周杰", {}]
- ["王磊", "下属", "李远", {}]
- ["王磊", "下属", "徐晓明", {}]
- ["陈燕", "下属", "刘颖", {}]
- ["陈燕", "下属", "黄志强", {}]
- ["周杰", "下属", "张华", {}]
- ["周杰", "下属", "李思", {}]
- ["韩梅", "团队成员", "王晓丽", {}]
- ["韩梅", "团队成员", "林涛", {}]
- ["韩梅", "团队成员", "刘倩", {}]
- ["韩梅", "团队成员", "赵天宇", {}]
- ["韩梅", "团队成员", "徐杰", {}]
- ["赵强", "下属", "孙玲", {}]
- ["赵强", "下属", "马超", {}]
- ["孙浩", "下属", "杜慧", {}]
- ["孙浩", "下属", "周雷", {}]
- ["浩瀚科技", "产品", "星云浏览器", {}]
- ["张婷", "贡献", "星云浏览器", {}]
- ["王磊", "贡献", "星云浏览器", {}]
- ["韩梅", "推广", "星云浏览器", {}]
- ["林涛", "支持", "星云浏览器推广", {}]
- ["赵强", "招募", "研发部人才", {}]
- ["孙浩", "资金支持", "星云浏览器", {}]
- ["浩瀚科技", "客户", "华为", {}]
- ["浩瀚科技", "客户", "小米", {}]
- ["浩瀚科技", "客户", "OPPO", {}]
- ["浩瀚科技", "合作伙伴", "京东商城", {}]
- ["李伟", "沟通", "各部门经理", {}]
- ["李伟", "邀请", "张婷", {"目的": "产品研发讨论"}]
- ["李伟", "认可", "韩梅市场推广方案", {}]
- ["赵强", "协作", "孙浩", {"目的": "管理人力和财力资源"}]2024-01-17 16:34:07 extract_kg.py [line:21] INFO	: request_to_ai res: Nodes:
- ["浩瀚科技", "公司", {"名称": "浩瀚科技"}]
- ["李伟", "人", {"姓名": "李伟", "职位": "总裁"}]
- ["张婷", "人", {"姓名": "张婷", "职位": "研发部部长"}]
- ["韩梅", "人", {"姓名": "韩梅", "职位": "市场部部长"}]
- ["赵强", "人", {"姓名": "赵强", "职位": "人事部部长"}]
- ["孙浩", "人", {"姓名": "孙浩", "职位": "财务部部长"}]
- ["王磊", "人", {"姓名": "王磊", "职位": "算法组组长"}]
- ["李远", "人", {"姓名": "李远", "职位": "资深工程师"}]
- ["徐晓明", "人", {"姓名": "徐晓明", "职位": "资深工程师"}]
- ["陈燕", "人", {"姓名": "陈燕", "职位": "软件开发组组长"}]
- ["刘颖", "人", {"姓名": "刘颖"}]
- ["黄志强", "人", {"姓名": "黄志强"}]
- ["周杰", "人", {"姓名": "周杰", "职位": "人工智能小组组长"}]
- ["张华", "人", {"姓名": "张华", "职位": "资深研究员"}]
- ["李思", "人", {"姓名": "李思", "职位": "工程师"}]
- ["王晓丽", "人", {"姓名": "王晓丽", "职位": "市场策划师"}]
- ["林涛", "人", {"姓名": "林涛", "职位": "数据分析师"}]
- ["刘倩", "人", {"姓名": "刘倩", "职位": "客户经理"}]
- ["赵天宇", "人", {"姓名": "赵天宇", "职位": "媒介专员"}]
- ["徐杰", "人", {"姓名": "徐杰", "职位": "网络营销师"}]
- ["孙玲", "人", {"姓名": "孙玲", "职位": "招聘专员"}]
- ["马超", "人", {"姓名": "马超", "职位": "员工关系主管"}]
- ["杜慧", "人", {"姓名": "杜慧", "职位": "会计师"}]
- ["周雷", "人", {"姓名": "周雷", "职位": "财务分析师"}]
- ["星云浏览器", "产品", {"名称": "星云浏览器"}]
- ["华为", "公司", {"名称": "华为"}]
- ["小米", "公司", {"名称": "小米"}]
- ["OPPO", "公司", {"名称": "OPPO"}]
- ["京东商城", "公司", {"名称": "京东商城"}]

Relationships:
- ["浩瀚科技", "总裁", "李伟", {}]
- ["浩瀚科技", "部门", "研发部", {}]
- ["浩瀚科技", "部门", "市场部", {}]
- ["浩瀚科技", "部门", "人事部", {}]
- ["浩瀚科技", "部门", "财务部", {}]
- ["研发部", "部门长", "张婷", {}]
- ["市场部", "部门长", "韩梅", {}]
- ["人事部", "部门长", "赵强", {}]
- ["财务部", "部门长", "孙浩", {}]
- ["研发部", "小组", "算法组", {}]
- ["研发部", "小组", "软件开发组", {}]
- ["研发部", "小组", "人工智能小组", {}]
- ["算法组", "组长", "王磊", {}]
- ["软件开发组", "组长", "陈燕", {}]
- ["人工智能小组", "组长", "周杰", {}]
- ["王磊", "下属", "李远", {}]
- ["王磊", "下属", "徐晓明", {}]
- ["陈燕", "下属", "刘颖", {}]
- ["陈燕", "下属", "黄志强", {}]
- ["周杰", "下属", "张华", {}]
- ["周杰", "下属", "李思", {}]
- ["韩梅", "团队成员", "王晓丽", {}]
- ["韩梅", "团队成员", "林涛", {}]
- ["韩梅", "团队成员", "刘倩", {}]
- ["韩梅", "团队成员", "赵天宇", {}]
- ["韩梅", "团队成员", "徐杰", {}]
- ["赵强", "下属", "孙玲", {}]
- ["赵强", "下属", "马超", {}]
- ["孙浩", "下属", "杜慧", {}]
- ["孙浩", "下属", "周雷", {}]
- ["浩瀚科技", "产品", "星云浏览器", {}]
- ["张婷", "贡献", "星云浏览器", {}]
- ["王磊", "贡献", "星云浏览器", {}]
- ["韩梅", "推广", "星云浏览器", {}]
- ["林涛", "支持", "星云浏览器推广", {}]
- ["赵强", "招募", "研发部人才", {}]
- ["孙浩", "资金支持", "星云浏览器", {}]
- ["浩瀚科技", "客户", "华为", {}]
- ["浩瀚科技", "客户", "小米", {}]
- ["浩瀚科技", "客户", "OPPO", {}]
- ["浩瀚科技", "合作伙伴", "京东商城", {}]
- ["李伟", "沟通", "各部门经理", {}]
- ["李伟", "邀请", "张婷", {"目的": "产品研发讨论"}]
- ["李伟", "认可", "韩梅市场推广方案", {}]
- ["赵强", "协作", "孙浩", {"目的": "管理人力和财力资源"}]
```

extract nodes and relationships

```json
{
  "action": "kg",
  "data": [
    {
      "nodes": [
        {
          "name": "浩瀚科技",
          "label": "公司",
          "properties": {
            "名称": "浩瀚科技"
          }
        },
        {
          "name": "李伟",
          "label": "人",
          "properties": {
            "姓名": "李伟",
            "职位": "总裁"
          }
        },
        {
          "name": "张婷",
          "label": "人",
          "properties": {
            "姓名": "张婷",
            "职位": "研发部部长"
          }
        },
        {
          "name": "韩梅",
          "label": "人",
          "properties": {
            "姓名": "韩梅",
            "职位": "市场部部长"
          }
        },
        {
          "name": "赵强",
          "label": "人",
          "properties": {
            "姓名": "赵强",
            "职位": "人事部部长"
          }
        },
        {
          "name": "孙浩",
          "label": "人",
          "properties": {
            "姓名": "孙浩",
            "职位": "财务部部长"
          }
        },
        {
          "name": "王磊",
          "label": "人",
          "properties": {
            "姓名": "王磊",
            "职位": "算法组组长"
          }
        },
        {
          "name": "李远",
          "label": "人",
          "properties": {
            "姓名": "李远",
            "职位": "资深工程师"
          }
        },
        {
          "name": "徐晓明",
          "label": "人",
          "properties": {
            "姓名": "徐晓明",
            "职位": "资深工程师"
          }
        },
        {
          "name": "陈燕",
          "label": "人",
          "properties": {
            "姓名": "陈燕",
            "职位": "软件开发组组长"
          }
        },
        {
          "name": "刘颖",
          "label": "人",
          "properties": {
            "姓名": "刘颖"
          }
        },
        {
          "name": "黄志强",
          "label": "人",
          "properties": {
            "姓名": "黄志强"
          }
        },
        {
          "name": "周杰",
          "label": "人",
          "properties": {
            "姓名": "周杰",
            "职位": "人工智能小组组长"
          }
        },
        {
          "name": "张华",
          "label": "人",
          "properties": {
            "姓名": "张华",
            "职位": "资深研究员"
          }
        },
        {
          "name": "李思",
          "label": "人",
          "properties": {
            "姓名": "李思",
            "职位": "工程师"
          }
        },
        {
          "name": "王晓丽",
          "label": "人",
          "properties": {
            "姓名": "王晓丽",
            "职位": "市场策划师"
          }
        },
        {
          "name": "林涛",
          "label": "人",
          "properties": {
            "姓名": "林涛",
            "职位": "数据分析师"
          }
        },
        {
          "name": "刘倩",
          "label": "人",
          "properties": {
            "姓名": "刘倩",
            "职位": "客户经理"
          }
        },
        {
          "name": "赵天宇",
          "label": "人",
          "properties": {
            "姓名": "赵天宇",
            "职位": "媒介专员"
          }
        },
        {
          "name": "徐杰",
          "label": "人",
          "properties": {
            "姓名": "徐杰",
            "职位": "网络营销师"
          }
        },
        {
          "name": "孙玲",
          "label": "人",
          "properties": {
            "姓名": "孙玲",
            "职位": "招聘专员"
          }
        },
        {
          "name": "马超",
          "label": "人",
          "properties": {
            "姓名": "马超",
            "职位": "员工关系主管"
          }
        },
        {
          "name": "杜慧",
          "label": "人",
          "properties": {
            "姓名": "杜慧",
            "职位": "会计师"
          }
        },
        {
          "name": "周雷",
          "label": "人",
          "properties": {
            "姓名": "周雷",
            "职位": "财务分析师"
          }
        },
        {
          "name": "星云浏览器",
          "label": "产品",
          "properties": {
            "名称": "星云浏览器"
          }
        },
        {
          "name": "华为",
          "label": "公司",
          "properties": {
            "名称": "华为"
          }
        },
        {
          "name": "小米",
          "label": "公司",
          "properties": {
            "名称": "小米"
          }
        },
        {
          "name": "OPPO",
          "label": "公司",
          "properties": {
            "名称": "OPPO"
          }
        },
        {
          "name": "京东商城",
          "label": "公司",
          "properties": {
            "名称": "京东商城"
          }
        }
      ],
      "relationships": [
        {
          "start": "浩瀚科技",
          "end": "李伟",
          "type": "总裁",
          "properties": {}
        },
        {
          "start": "浩瀚科技",
          "end": "研发部",
          "type": "部门",
          "properties": {}
        },
        {
          "start": "浩瀚科技",
          "end": "市场部",
          "type": "部门",
          "properties": {}
        },
        {
          "start": "浩瀚科技",
          "end": "人事部",
          "type": "部门",
          "properties": {}
        },
        {
          "start": "浩瀚科技",
          "end": "财务部",
          "type": "部门",
          "properties": {}
        },
        {
          "start": "研发部",
          "end": "张婷",
          "type": "部门长",
          "properties": {}
        },
        {
          "start": "市场部",
          "end": "韩梅",
          "type": "部门长",
          "properties": {}
        },
        {
          "start": "人事部",
          "end": "赵强",
          "type": "部门长",
          "properties": {}
        },
        {
          "start": "财务部",
          "end": "孙浩",
          "type": "部门长",
          "properties": {}
        },
        {
          "start": "研发部",
          "end": "算法组",
          "type": "小组",
          "properties": {}
        },
        {
          "start": "研发部",
          "end": "软件开发组",
          "type": "小组",
          "properties": {}
        },
        {
          "start": "研发部",
          "end": "人工智能小组",
          "type": "小组",
          "properties": {}
        },
        {
          "start": "算法组",
          "end": "王磊",
          "type": "组长",
          "properties": {}
        },
        {
          "start": "软件开发组",
          "end": "陈燕",
          "type": "组长",
          "properties": {}
        },
        {
          "start": "人工智能小组",
          "end": "周杰",
          "type": "组长",
          "properties": {}
        },
        {
          "start": "王磊",
          "end": "李远",
          "type": "下属",
          "properties": {}
        },
        {
          "start": "王磊",
          "end": "徐晓明",
          "type": "下属",
          "properties": {}
        },
        {
          "start": "陈燕",
          "end": "刘颖",
          "type": "下属",
          "properties": {}
        },
        {
          "start": "陈燕",
          "end": "黄志强",
          "type": "下属",
          "properties": {}
        },
        {
          "start": "周杰",
          "end": "张华",
          "type": "下属",
          "properties": {}
        },
        {
          "start": "周杰",
          "end": "李思",
          "type": "下属",
          "properties": {}
        },
        {
          "start": "韩梅",
          "end": "王晓丽",
          "type": "团队成员",
          "properties": {}
        },
        {
          "start": "韩梅",
          "end": "林涛",
          "type": "团队成员",
          "properties": {}
        },
        {
          "start": "韩梅",
          "end": "刘倩",
          "type": "团队成员",
          "properties": {}
        },
        {
          "start": "韩梅",
          "end": "赵天宇",
          "type": "团队成员",
          "properties": {}
        },
        {
          "start": "韩梅",
          "end": "徐杰",
          "type": "团队成员",
          "properties": {}
        },
        {
          "start": "赵强",
          "end": "孙玲",
          "type": "下属",
          "properties": {}
        },
        {
          "start": "赵强",
          "end": "马超",
          "type": "下属",
          "properties": {}
        },
        {
          "start": "孙浩",
          "end": "杜慧",
          "type": "下属",
          "properties": {}
        },
        {
          "start": "孙浩",
          "end": "周雷",
          "type": "下属",
          "properties": {}
        },
        {
          "start": "浩瀚科技",
          "end": "星云浏览器",
          "type": "产品",
          "properties": {}
        },
        {
          "start": "张婷",
          "end": "星云浏览器",
          "type": "贡献",
          "properties": {}
        },
        {
          "start": "王磊",
          "end": "星云浏览器",
          "type": "贡献",
          "properties": {}
        },
        {
          "start": "韩梅",
          "end": "星云浏览器",
          "type": "推广",
          "properties": {}
        },
        {
          "start": "林涛",
          "end": "星云浏览器推广",
          "type": "支持",
          "properties": {}
        },
        {
          "start": "赵强",
          "end": "研发部人才",
          "type": "招募",
          "properties": {}
        },
        {
          "start": "孙浩",
          "end": "星云浏览器",
          "type": "资金支持",
          "properties": {}
        },
        {
          "start": "浩瀚科技",
          "end": "华为",
          "type": "客户",
          "properties": {}
        },
        {
          "start": "浩瀚科技",
          "end": "小米",
          "type": "客户",
          "properties": {}
        },
        {
          "start": "浩瀚科技",
          "end": "OPPO",
          "type": "客户",
          "properties": {}
        },
        {
          "start": "浩瀚科技",
          "end": "京东商城",
          "type": "合作伙伴",
          "properties": {}
        },
        {
          "start": "李伟",
          "end": "各部门经理",
          "type": "沟通",
          "properties": {}
        },
        {
          "start": "李伟",
          "end": "张婷",
          "type": "邀请",
          "properties": {
            "目的": "产品研发讨论"
          }
        },
        {
          "start": "李伟",
          "end": "韩梅市场推广方案",
          "type": "认可",
          "properties": {}
        },
        {
          "start": "赵强",
          "end": "孙浩",
          "type": "协作",
          "properties": {
            "目的": "管理人力和财力资源"
          }
        }
      ]
    }
  ]
}
```


## test case 2

prompts

```text
你是一名数据科学家，在一家正在构建图形数据库的公司工作。您的任务是从文本数据中提取信息并将其转换为图形数据库中适用的格式。
请以[ENTITY_ID, TYPE, PROPERTIES]的形式提取一组节点，并以[ENTITY_ID_1, RELATIONSHIP, ENTITY_ID_2, PROPERTIES]的形式提取一组关系。
需要注意，ENTITY_ID_1和ENTITY_ID_2应当具有匹配ENTITY_ID的节点存在。如果你不能将一个关系与一对节点配对，那就不要添加它。
当您找到想要添加的节点或关系时，请尝试为其创建描述实体的抽象TYPE，您也可以将其视为标签。请直接输出您提取出的节点和关系，不要输出任何分析过程。

例子:

文本数据:李薇是律师，今年25岁，Bob从2001年起就是她的室友。Bob是一名记者。李薇拥有网页www.liwei.com, Bob拥有网页www.bob.com。
Nodes:
- ["LiWei", "Person", {"age":25, "job":"律师"、"name":"李薇"}]
- ["Bob", "Person", {"job":"记者","name":"Bob"}]
- ["liwei.com", "Website", {"url": "www.liwei.com"}]
- ["bob.com", "Website", {"url": "www.bob.com"}]
Relationships:
- ["LiWei", "roommate", "Bob", {"start":2021}]
- ["LiWei", "owns", "liwei.com", {}]
- ["Bob", "owns", "bob.com", {}]
```

AI Output

```text
Nodes:
- ["HaohanTech", "Company", {"name":"浩瀚科技"}]
- ["LiWei", "Person", {"job":"总裁", "name":"李伟"}]
- ["R&D", "Department", {"name":"研发部"}]
- ["Marketing", "Department", {"name":"市场部"}]
- ["HR", "Department", {"name":"人事部"}]
- ["Finance", "Department", {"name":"财务部"}]
- ["ZhangTing", "Person", {"job":"研发部部长", "name":"张婷"}]
- ["HanMei", "Person", {"job":"市场部部长", "name":"韩梅"}]
- ["ZhaoQiang", "Person", {"job":"人事部部长", "name":"赵强"}]
- ["SunHao", "Person", {"job":"财务部部长", "name":"孙浩"}]
- ["StarCloudBrowser", "Product", {"name":"星云浏览器"}]
- ["Huawei", "Company", {"name":"华为"}]
- ["Xiaomi", "Company", {"name":"小米"}]
- ["OPPO", "Company", {"name":"OPPO"}]
- ["JingdongMall", "Company", {"name":"京东商城"}]

Relationships:
- ["LiWei", "works_for", "HaohanTech", {"position":"总裁"}]
- ["ZhangTing", "works_for", "HaohanTech", {"position":"研发部部长"}]
- ["HanMei", "works_for", "HaohanTech", {"position":"市场部部长"}]
- ["ZhaoQiang", "works_for", "HaohanTech", {"position":"人事部部长"}]
- ["SunHao", "works_for", "HaohanTech", {"position":"财务部部长"}]
- ["HaohanTech", "has_department", "R&D", {}]
- ["HaohanTech", "has_department", "Marketing", {}]
- ["HaohanTech", "has_department", "HR", {}]
- ["HaohanTech", "has_department", "Finance", {}]
- ["HaohanTech", "produces", "StarCloudBrowser", {}]
- ["Huawei", "uses", "StarCloudBrowser", {}]
- ["Xiaomi", "uses", "StarCloudBrowser", {}]
- ["OPPO", "uses", "StarCloudBrowser", {}]
- ["HaohanTech", "partners_with", "JingdongMall", {}]
- ["LiWei", "collaborates_with", "ZhangTing", {}]
- ["LiWei", "collaborates_with", "HanMei", {}]
- ["ZhaoQiang", "collaborates_with", "SunHao", {}]
```

extracted json data

```json
{
  "action": "kg",
  "data": {
    "nodes": [
      {
        "name": "HaohanTech",
        "label": "Company",
        "properties": {
          "name": "浩瀚科技"
        }
      },
      {
        "name": "LiWei",
        "label": "Person",
        "properties": {
          "job": "总裁",
          "name": "李伟"
        }
      },
      {
        "name": "R&D",
        "label": "Department",
        "properties": {
          "name": "研发部"
        }
      },
      {
        "name": "Marketing",
        "label": "Department",
        "properties": {
          "name": "市场部"
        }
      },
      {
        "name": "HR",
        "label": "Department",
        "properties": {
          "name": "人事部"
        }
      },
      {
        "name": "Finance",
        "label": "Department",
        "properties": {
          "name": "财务部"
        }
      },
      {
        "name": "ZhangTing",
        "label": "Person",
        "properties": {
          "job": "研发部部长",
          "name": "张婷"
        }
      },
      {
        "name": "HanMei",
        "label": "Person",
        "properties": {
          "job": "市场部部长",
          "name": "韩梅"
        }
      },
      {
        "name": "ZhaoQiang",
        "label": "Person",
        "properties": {
          "job": "人事部部长",
          "name": "赵强"
        }
      },
      {
        "name": "SunHao",
        "label": "Person",
        "properties": {
          "job": "财务部部长",
          "name": "孙浩"
        }
      },
      {
        "name": "StarCloudBrowser",
        "label": "Product",
        "properties": {
          "name": "星云浏览器"
        }
      },
      {
        "name": "Huawei",
        "label": "Company",
        "properties": {
          "name": "华为"
        }
      },
      {
        "name": "Xiaomi",
        "label": "Company",
        "properties": {
          "name": "小米"
        }
      },
      {
        "name": "OPPO",
        "label": "Company",
        "properties": {
          "name": "OPPO"
        }
      },
      {
        "name": "JingdongMall",
        "label": "Company",
        "properties": {
          "name": "京东商城"
        }
      }
    ],
    "relationships": []
  }
}
```

cypher

```json
{
  "action": "cypher",
  "data": "CALL apoc.load.json("file:/path_to_your_json_file.json") YIELD value AS data\nUNWIND data.nodes AS node\nMERGE (n:Node {name: node.name})\nSET n += node.properties\nSET n: `node.label`\n\nUNWIND data.relationships AS rel\nMATCH (start:Node {name: rel.start}), (end:Node {name: rel.end})\nMERGE (start)-[r:RELATIONSHIP {type: rel.type}]->(end)\nSET r += rel.properties"
}
```

```json
{"nodes": [{"name": "HaohanTech", "label": "Company", "properties": {"name": "浩瀚科技"}}, {"name": "LiWei", "label": "Person", "properties": {"job": "总裁", "name": "李伟"}}, {"name": "ZhangTing", "label": "Person", "properties": {"job": "研发部部长", "name": "张婷"}}, {"name": "HanMei", "label": "Person", "properties": {"job": "市场部部长", "name": "韩梅"}}, {"name": "ZhaoQiang", "label": "Person", "properties": {"job": "人事部部长", "name": "赵强"}}, {"name": "SunHao", "label": "Person", "properties": {"job": "财务部部长", "name": "孙浩"}}, {"name": "XingyunBrowser", "label": "Product", "properties": {"name": "星云浏览器"}}, {"name": "Huawei", "label": "Company", "properties": {"name": "华为"}}, {"name": "Xiaomi", "label": "Company", "properties": {"name": "小米"}}, {"name": "OPPO", "label": "Company", "properties": {"name": "OPPO"}}, {"name": "JingdongMall", "label": "Company", "properties": {"name": "京东商城"}}], "relationships": [{"start": "HaohanTech", "end": "LiWei", "type": "led_by", "properties": {}}, {"start": "HaohanTech", "end": "ZhangTing", "type": "has_department_head", "properties": {"department": "研发部"}}, {"start": "HaohanTech", "end": "HanMei", "type": "has_department_head", "properties": {"department": "市场部"}}, {"start": "HaohanTech", "end": "ZhaoQiang", "type": "has_department_head", "properties": {"department": "人事部"}}, {"start": "HaohanTech", "end": "SunHao", "type": "has_department_head", "properties": {"department": "财务部"}}, {"start": "HaohanTech", "end": "XingyunBrowser", "type": "produces", "properties": {}}, {"start": "Huawei", "end": "XingyunBrowser", "type": "uses", "properties": {}}, {"start": "Xiaomi", "end": "XingyunBrowser", "type": "uses", "properties": {}}, {"start": "OPPO", "end": "XingyunBrowser", "type": "uses", "properties": {}}, {"start": "HaohanTech", "end": "JingdongMall", "type": "cooperates_with", "properties": {}}, {"start": "LiWei", "end": "ZhangTing", "type": "communicates_with", "properties": {}}, {"start": "LiWei", "end": "HanMei", "type": "communicates_with", "properties": {}}, {"start": "LiWei", "end": "ZhaoQiang", "type": "communicates_with", "properties": {}}, {"start": "LiWei", "end": "SunHao", "type": "communicates_with", "properties": {}}]}
```