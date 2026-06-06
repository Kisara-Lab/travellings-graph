"""将 output/ 下的 JSON 数据转换为 CSV 格式，便于开源和二次分析。"""
import json
import csv
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT = os.path.join(BASE, "output")
OUTPUT = os.path.join(BASE, "csv")
os.makedirs(OUTPUT, exist_ok=True)


def load(name):
    with open(os.path.join(INPUT, name), "r", encoding="utf-8") as f:
        return json.load(f)


def write_csv(name, rows, fieldnames):
    path = os.path.join(OUTPUT, name)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"  {name}: {len(rows)} rows, {len(fieldnames)} cols")


def convert_nodes():
    data = load("nodes.json")
    write_csv("nodes.csv", data, ["id", "name", "tag"])


def convert_edges():
    data = load("edges.json")
    write_csv("edges.csv", data, ["source", "target"])


def convert_activity():
    data = load("activity.json")
    fields = ["domain", "url", "feed_url", "last_update",
              "posts_3m", "posts_6m", "posts_1y", "total_posts", "level"]
    write_csv("activity.csv", data["sites"], fields)


def convert_response_times():
    data = load("response_times.json")
    fields = ["domain", "url", "status", "time_ms", "error"]
    write_csv("response_times.csv", data["all_results"], fields)


def convert_infra():
    data = load("infra.json")
    rows = []
    for item in data["all_results"]:
        rows.append({
            "domain": item["domain"],
            "url": item["url"],
            "https": item["https"],
            "providers": "; ".join(item.get("providers") or []),
            "server": item.get("server") or "",
        })
    write_csv("infra.csv", rows, ["domain", "url", "https", "providers", "server"])


def convert_seo():
    data = load("seo.json")
    fields = ["domain", "url", "title", "title_len", "description", "desc_len",
              "og_title", "og_description", "og_image", "og_url",
              "twitter_card", "canonical", "viewport",
              "robots_txt", "sitemap_xml", "h1_count", "img_no_alt", "score", "error"]
    write_csv("seo.csv", data["all_results"], fields)


def convert_social():
    data = load("social.json")
    # 收集所有出现过的平台
    platforms = set()
    for item in data["all_results"]:
        platforms.update((item.get("accounts") or {}).keys())
    platforms = sorted(platforms)

    rows = []
    for item in data["all_results"]:
        row = {"domain": item["domain"], "url": item["url"]}
        accounts = item.get("accounts") or {}
        for p in platforms:
            row[p] = accounts.get(p, "")
        rows.append(row)
    write_csv("social.csv", rows, ["domain", "url"] + platforms)


def convert_communities():
    data = load("communities.json")
    if isinstance(data, list):
        rows = data
    elif "communities" in data:
        rows = []
        for comm in data["communities"]:
            cid = comm.get("id", "")
            for member in comm.get("members", []):
                rows.append({"community_id": cid, "domain": member})
    else:
        rows = []
        for k, v in data.items():
            if isinstance(v, list):
                for member in v:
                    if isinstance(member, str):
                        rows.append({"community_id": k, "domain": member})
                    elif isinstance(member, dict):
                        member["community_id"] = k
                        rows.append(member)
    if rows:
        write_csv("communities.csv", rows, list(rows[0].keys()))


def convert_external_links():
    data = load("external_links.json")
    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        rows = data.get("links", data.get("all_results", []))
        if not rows and any(isinstance(v, list) for v in data.values()):
            for v in data.values():
                if isinstance(v, list) and v:
                    rows = v
                    break
    if rows and isinstance(rows[0], dict):
        write_csv("external_links.csv", rows, list(rows[0].keys()))


def convert_stats():
    data = load("stats.json")
    if isinstance(data, dict):
        rows = [data]
        write_csv("stats.csv", rows, list(data.keys()))


def convert_icp_geo():
    data = load("icp_geo.json")
    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        rows = data.get("sites", data.get("all_results", []))
    if rows and isinstance(rows[0], dict):
        write_csv("icp_geo.csv", rows, list(rows[0].keys()))


def convert_platforms():
    data = load("platforms.json")
    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        rows = data.get("platforms", data.get("sites", data.get("all_results", [])))
    if rows and isinstance(rows[0], dict):
        write_csv("platforms.csv", rows, list(rows[0].keys()))


if __name__ == "__main__":
    print("Converting JSON → CSV...")
    convert_nodes()
    convert_edges()
    convert_activity()
    convert_response_times()
    convert_infra()
    convert_seo()
    convert_social()
    convert_communities()
    convert_external_links()
    convert_stats()
    convert_icp_geo()
    convert_platforms()
    print(f"\nDone! CSV files saved to: {OUTPUT}")
