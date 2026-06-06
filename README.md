# 开往网络图谱 Travellings Graph

基于 [开往](https://www.travellings.cn/) 成员站点的网络关系图谱与多维度分析。

**在线预览**: https://kisara-lab.github.io/travellings-graph/

## 采集日期

2026-06-06（一次性快照，非持续更新）

## 数据概览

| 指标 | 数值 |
|------|------|
| 成员站点 | 1519 |
| 成功爬取 | 1229 |
| 站间链接 | 4115 |
| 社区检测 | 25 个 |
| RSS 覆盖 | 62% |
| HTTPS 覆盖 | 99.9% |

## 采集方法

### Phase 1 — 成员列表

从 `https://api.travellings.cn/all` 获取全部成员域名与 URL。

### Phase 2 — 双层爬取

对每个成员站执行两层爬取：
1. **首页**：提取所有 `<a>` 链接，匹配成员域名建立有向边
2. **友链页**：通过关键词（友链/友情链接/links/blogroll 等）定位站内友链页面，最多跟进 3 个候选页，重复提取

并发 50，超时 15 秒，使用 asyncio + aiohttp。

### Phase 3 — 多维度分析

| 脚本 | 分析内容 | 方法 |
|------|----------|------|
| `analyze.py` | PageRank / 度分布 / 社区检测 | NetworkX + Louvain |
| `detect_platform.py` | 建站平台 | meta generator + HTML 模式匹配 |
| `detect_icp.py` | ICP 备案地理 | 页面正文正则匹配备案号 |
| `detect_external.py` | 外部链接 | 首页出链去重 + 分类 |
| `crawl_orgs.py` | 博客组织生态 | 三层外爬 + 已知组织域名/关键词匹配 |
| `detect_activity.py` | 更新频率 | RSS/Atom feed 解析，统计近 3/6/12 月发文 |
| `detect_response.py` | 响应时间 | HEAD 请求测速（东京节点） |
| `detect_infra.py` | HTTPS / CDN / Server | HTTP 响应头分析 |
| `detect_seo.py` | SEO 健康度 | title/desc/OG/robots/sitemap 检测 |
| `detect_social.py` | 社交账号 | 首页 + 关于页链接模式提取 |

## 数据结构

```
output/
├── nodes.json              # 节点（domain, url, tag, community）
├── edges.json              # 有向边（source → target）
├── rankings.json           # 入度/出度/PageRank Top 20
├── degree_distribution.json
├── communities.json        # Louvain 社区划分
├── tag_heatmap.json
├── stats.json
├── platforms.json          # 建站平台分布
├── icp_geo.json            # ICP 备案省份分布
├── external_links.json     # 外部链接统计
├── org_network.json        # 博客组织关系网络
├── activity.json           # RSS 活跃度数据
├── response_times.json     # 响应时间测量
├── infra.json              # HTTPS / CDN / Server
├── seo.json                # SEO 健康度评分
└── social.json             # 社交平台分布
```

## 可视化页面

| 页面 | 内容 |
|------|------|
| index.html | D3 力导向图（节点=站点，边=链接关系） |
| dashboard.html | 排名 / 度分布 / 标签热图 / 社区 / 平台 / ICP |
| external.html | 外链分类气泡图 + 排行 |
| orgs.html | 博客组织关系力导向图 + 交叉矩阵 |
| activity.html | RSS 活跃度 + 响应时间统计 |
| infra.html | HTTPS 覆盖 / CDN 托管商 / Web Server |
| profile.html | SEO 健康度 + 社交平台画像 |

## 技术栈

- 爬虫：Python 3.11 + asyncio + aiohttp + BeautifulSoup4
- 存储：SQLite (aiosqlite)
- 分析：NetworkX + NumPy + SciPy
- 可视化：D3.js v7
- 部署：GitHub Pages

## 免责声明

1. 本项目仅用于学术研究和技术探索，数据来源为公开可访问的网页内容
2. 使用合理的并发控制和请求间隔，尽量减少对目标站点的影响
3. 数据为 2026-06-06 的一次性快照，不保证准确性和时效性
4. 本项目与开往官方无关，不代表开往项目的立场或观点
5. 如果您是成员站站主且不希望您的站点出现在分析中，请提交 Issue 说明，我们会及时移除
6. 本项目不存储任何用户隐私数据，所有分析基于公开页面内容
7. 请勿将本项目数据用于商业用途或任何可能侵犯他人权益的场景

## License

MIT
