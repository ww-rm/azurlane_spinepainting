---
title: azurlane_spinepainting
permalink: /index.html
---

[![Test](https://github.com/ww-rm/azurlane_spinepainting/actions/workflows/test.yaml/badge.svg)](https://github.com/ww-rm/azurlane_spinepainting/actions/workflows/test.yaml)

这是碧蓝航线动态立绘资源仓库.

点击返回[网站首页](/).

---

## 获取资源索引

请求:

`/azurlane_spinepainting/index.json`

响应:

```json
{
    "<shipName>": {
        "chName": "<舰娘中文名>",
        "hxName[可选]": "<舰娘和谐名>",
        "skins": {
            "<skinName>": {
                "chName": "<皮肤中文名>",
                "spines": [
                    {
                        "skelName": "<skel文件名>",
                        "atlasName": "<atlas文件名>",
                        "pages": ["<png1文件名>", "<png2文件名>"]
                    }
                ]
            }
        }
    }
}
```

Pydantic 解析示例:

```python
class Spine(BaseModel):
    skelName: str
    atlasName: str
    pages: List[str]

class Skin(BaseModel):
    chName: str
    spines: List[Spine]

class Ship(BaseModel):
    chName: str
    hxName: Optional[str] = None
    skins: Dict[str, Skin]

class ShipData(BaseModel):
    root: Dict[str, Ship]
```

访问测试:

- [/azurlane_spinepainting/index.json](/azurlane_spinepainting/index.json)

## 加载资源文件

请求:

`/azurlane_spinepainting/<shipName>/<skinName>/<文件名>`

访问测试:

- [/azurlane_spinepainting/yanzhan/yanzhan_g/yanzhan_g.skel](/azurlane_spinepainting/yanzhan/yanzhan_g/yanzhan_g.skel)
- [/azurlane_spinepainting/yanzhan/yanzhan_g/yanzhan_g.atlas](/azurlane_spinepainting/yanzhan/yanzhan_g/yanzhan_g.atlas)
- [/azurlane_spinepainting/yanzhan/yanzhan_g/yanzhan_g.png](/azurlane_spinepainting/yanzhan/yanzhan_g/yanzhan_g.png)
