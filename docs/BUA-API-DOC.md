#### 1. 创建一轮测试的问题
```
curl 'https://api.bua.sh/round/new?agent_name=solflare-1.11'
```
参数
| field | type | desc | optional |
| --- | --- | --- | --- |
| agent_name | string | Agent名称 | true |

响应
```
{
  "agent_kp": "测试钱包私钥",
  "agent_name": "Agent名称",
  "agent_pubkey": "测试钱包公钥",
  "created_at": "创建时间",
  "id": "本轮测试ID(RPC传入)",
  "prompt": {
    "问题ID(RPC传入)": {
      "prompt": "提示词"
    }
  }
}
```

#### 2. 获取指定轮次的信息
```
curl 'https://api.bua.sh/round/get/694a0f20d7597851ec47b40c?full=true'
```
参数
| field | type | desc | optional |
| --- | --- | --- | --- |
| full | bool | 是否显示每个问题的验证信息 | true |

响应
```
{
  "agent_kp": "测试钱包私钥",
  "agent_name": "Agent名称",
  "agent_pubkey": "测试钱包公钥",
  "created_at": "创建时间",
  "id": "本轮测试ID(RPC传入)",
  "prompt": {
    "问题ID(RPC传入)": {
      "prompt": "提示词"
    }
  }
}
```

#### 3. 分页获取轮次的信息
```
curl 'https://api.bua.sh/round/list/{page}/{page_size}'
```
参数
| field | type | desc | optional |
| --- | --- | --- | --- |
| page | int | 页码 | false |
| page_size | int | 每页数量 | false |

响应
```
[
    {
    "agent_kp": "测试钱包私钥",
    "agent_name": "Agent名称",
    "agent_pubkey": "测试钱包公钥",
    "created_at": "创建时间",
    "id": "本轮测试ID(RPC传入)",
    "prompt": {
        "问题ID(RPC传入)": {
        "prompt": "提示词"
        }
    }
    }
]

```

#### 3. RPC
```
https://api.bua.sh/rpc/solana?round=69490d5140c972633170de53&question=69490d5140c972633170de42
```
测评提交交易时，round和question参数根据测试轮次传入，每个问题都必须传入正确的id，否则无法正确计算分数，请求方法跟普通RPC一样，可以直接当正常RPC使用