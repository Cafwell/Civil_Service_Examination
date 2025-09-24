"""
成语搜索与释义工具

本程序是一个集成语释义查询和网络搜索功能于一体的工具。主要功能包括：

从星光公考网站获取成语的详细解释和补充分析（需要cookies登录才能使用）

在人民网、光明网、新华网等权威媒体网站中搜索成语的使用实例（可以自定义）

格式化输出搜索结果，突出显示关键词
"""


import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import re
import random


class BaiduSearchCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.baidu.com/',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_idiom_meaning(self, idiom, cookies_str):
        """
        使用浏览器cookies获取成语解释
        """
        url = f"https://www.xingguanggongkao.com/pc/words/search.html?keywords={idiom}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.xingguanggongkao.com/'
        }

        # 将cookies字符串转换为字典
        cookies = {}
        for cookie in cookies_str.split('; '):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key] = value

        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        if response.status_code != 200:
            print(f"请求失败，状态码：{response.status_code}")
            return None

        response.encoding = 'utf-8'

        # 检查是否还是跳转登录页面
        if "请先登录" in response.text:
            print("Cookies可能已过期或无效")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        result = {'idiom': idiom}

        # 查找解释部分
        explain_div = soup.find('div', class_='words-search-explain')
        if not explain_div:
            return None

        # 获取基本解释
        basic_explain = explain_div.get_text(strip=True)
        result['基本解释'] = basic_explain

        # 查找补充分析部分
        analysis_div = soup.find('div', class_='words-search-analysis')
        if analysis_div:
            # 获取分析值部分
            analysis_value = analysis_div.find('div', class_='words-search-analysis-value')
            if analysis_value:
                # 处理HTML中的换行标签<br>，将其转换为换行符
                for br in analysis_value.find_all('br'):
                    br.replace_with('\n')

                # 获取处理后的文本
                analysis_text = analysis_value.get_text()

                # 清理文本，保留换行
                analysis_text = re.sub(r'[ \t]+', ' ', analysis_text)  # 压缩多个空格和制表符
                analysis_text = re.sub(r'\n\s*\n', '\n\n', analysis_text)  # 保留段落间的空行
                analysis_text = analysis_text.strip()

                result['补充分析'] = analysis_text

        return result

    def format_idiom_meaning(self, meaning_dict):
        """
        格式化成语解释输出，保留换行
        """
        if not meaning_dict:
            return None

        formatted = []
        idiom = meaning_dict.get('idiom', '')

        formatted.append(f"【{idiom}】")

        # 基本解释
        if '基本解释' in meaning_dict:
            formatted.append(f"解释：{meaning_dict['基本解释']}")

        # 补充分析（如果有）
        if '补充分析' in meaning_dict:
            formatted.append("")  # 空行
            formatted.append(meaning_dict['补充分析'])

        return '\n'.join(formatted)

    def extract_relevant_sentence(self, text, keyword):
        """
        智能提取包含关键词的相关句子
        """
        if keyword not in text:
            return ""

        sentences = re.split(r'[。！？|]', text)

        keyword_sentences = [s.strip() for s in sentences if keyword in s and len(s.strip()) > 0]

        if keyword_sentences:
            relevant_sentence = keyword_sentences[0]

            keyword_pos = relevant_sentence.find(keyword)
            if keyword_pos <= 10:
                first_sentence = sentences[0].strip() if sentences else ""
                if first_sentence and keyword in first_sentence:
                    return first_sentence + "。"
                else:
                    return relevant_sentence + "。"
            else:
                return relevant_sentence + "。"

        keyword_index = text.find(keyword)
        if keyword_index >= 0:
            start = max(0, keyword_index - 50)
            end = min(len(text), keyword_index + len(keyword) + 50)

            period_before = text.rfind('。', 0, keyword_index)
            if period_before > start:
                start = period_before + 1

            period_after = text.find('。', keyword_index)
            if period_after > 0 and period_after < end:
                end = period_after + 1

            extracted = text[start:end].strip()

            if keyword in extracted:
                return extracted

        keyword_index = text.find(keyword)
        if keyword_index >= 0:
            start = max(0, keyword_index - 30)
            end = min(len(text), keyword_index + len(keyword) + 30)
            return text[start:end].strip()

        return ""

    def build_search_url(self, keyword, site_domain):
        """
        构建搜索URL
        """
        inurl_query = f"inurl:{site_domain} {keyword}"
        encoded_query = urllib.parse.quote(inurl_query)
        url = f"https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&tn=baidu&wd={encoded_query}&rn=20"
        return url

    def search_baidu(self, keyword, site_name, site_domain):
        """
        搜索百度并返回结果
        """
        url = self.build_search_url(keyword, site_domain)

        print(f"搜索 {site_name}...")

        try:
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'

            if response.status_code == 200:
                return self.parse_baidu_results(response.text, keyword)
            else:
                print(f"请求失败，状态码：{response.status_code}")
                return []

        except Exception as e:
            print(f"搜索过程中出现错误：{e}")
            return []

    def parse_baidu_results(self, html_content, keyword):
        """
        解析百度搜索结果页面
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []

        containers = soup.find_all('div', class_='c-container')

        for container in containers:
            result = self.extract_result_info(container, keyword)
            if result:
                results.append(result)

        return results

    def extract_result_info(self, container, keyword):
        """
        从单个结果容器中提取信息
        """
        try:
            title_elem = container.find('h3')
            if not title_elem:
                return None

            title = title_elem.get_text().strip()

            abstract = None
            abstract_selectors = [
                'span.summary-text_560AW',
                'div.cu-line-clamp-2 span.summary-text_560AW',
                'div.c-abstract',
                'div.content-right_8Zs40',
                'span.content-right_8Zs40'
            ]

            for selector in abstract_selectors:
                abstract_elem = container.select_one(selector)
                if abstract_elem:
                    abstract = abstract_elem.get_text().strip()
                    break

            if not abstract:
                return None

            abstract = re.sub(r'\s+', ' ', abstract).strip()

            if keyword in abstract and len(abstract) > 10:
                extracted_abstract = self.extract_relevant_sentence(abstract, keyword)

                if not extracted_abstract:
                    extracted_abstract = abstract[:100] + "..." if len(abstract) > 100 else abstract

                return {
                    'title': title,
                    'abstract': extracted_abstract
                }

        except Exception as e:
            print(f"提取结果信息时出错：{e}")

        return None

    def search_multiple_sites(self, keyword, sites):
        """
        在多个网站中搜索关键词
        """
        all_results = {}

        for site_name, site_domain in sites.items():
            results = self.search_baidu(keyword, site_name, site_domain)
            all_results[site_name] = results

            print(f"{site_name} 找到 {len(results)} 条结果")

            time.sleep(random.uniform(2, 4))

        return all_results

    def format_results(self, results, keyword, idiom_meaning=None):
        """
        格式化输出结果
        """
        output = []

        # 添加成语解释
        if idiom_meaning:
            output.append("成语解释:")
            output.append("-" * 40)
            output.append(idiom_meaning)
            output.append("")

        output.append(f"搜索关键词: {keyword}")
        output.append("=" * 60)

        for site_name, site_results in results.items():
            output.append(f"\n{site_name}结果（{len(site_results)}条）:")

            if not site_results:
                output.append("  未找到相关结果")
                continue

            for i, result in enumerate(site_results, 1):
                abstract = result['abstract']
                highlighted_abstract = abstract.replace(keyword, f"【{keyword}】")
                output.append(f"{i}. {highlighted_abstract}")

        return '\n'.join(output)


def main():
    # 三个要搜索的网站，可以自定义
    official_media_sites = {
        '人民网': 'people.com.cn',
        '光明网': 'gmw.cn',
        '新华网': 'xinhuanet.com'
    }
    # 你自己的星光公考cookies
    cookies_str = ""
    crawler = BaiduSearchCrawler()

    while True:
        print("\n" + "=" * 30)
        print("成语/词语搜索")
        print("=" * 30)
        print("请输入要搜索的成语/词语（输入'quit'退出）:")
        keyword = input().strip()
        if keyword.lower() == 'quit':
            break
        if not keyword:
            print("请输入有效的关键词")
            continue

        # 获取成语解释
        idiom_meaning = crawler.get_idiom_meaning(keyword, cookies_str)
        if idiom_meaning:
            formatted = crawler.format_idiom_meaning(idiom_meaning)
            print("\n=== 成语/词语释义 ===")
            print(formatted)
        else:
            print("未找到该成语的解释")

        print("=" * 50)
        time.sleep(1)

        print(f"\n开始搜索关键词: {keyword}")
        print("请稍候..." + "\n")
        # 搜索所有网站
        results = crawler.search_multiple_sites(keyword, official_media_sites)

        # 格式化输出
        output = crawler.format_results(results, keyword)
        print("\n" + "=" * 50)
        print(output)
        print("=" * 50)

        # 询问是否继续
        print("\n是否继续搜索？(y/n):")
        continue_search = input().strip().lower()
        if continue_search != 'y':
            break


if __name__ == "__main__":
    main()