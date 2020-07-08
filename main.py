import time

import htmlmin
import matplotlib.pyplot as plt
import networkx as nx
from selenium import webdriver
from .element_node import ElementNode

# parser = argparse.ArgumentParser()
# parser.add_argument("location", help="location of the python file whose graph is to be added")
# args = parser.parse_args()

# html_text = "<html><head><title>This is title</title></head><body><h1>Heading</h1><p>Paragraph<b>Bold</b><br/></p></body></html>"
driver = webdriver.Chrome()
driver.get('http://stag.quartic.ai')
driver.find_element_by_id("email").send_keys("diptman@quartic.ai")
driver.find_element_by_id("password").send_keys("abc@1234")
driver.find_element_by_css_selector("button[class='btn btn-info btn-lg w-100']").click()
time.sleep(20)
page_source = driver.page_source
html_text = htmlmin.minify(page_source, remove_empty_space=True)


G = nx.Graph()
nodes = []
node_names = []

parent_node = None

i = 0
while len(html_text) > 0:
    start_key_pos = html_text.find("<")
    stop_key_pos = html_text.find(">")

    if stop_key_pos > html_text.find("/") > start_key_pos:
        if html_text.find("/") - start_key_pos == 1:
            graph_child = html_text[html_text.find("/") + 1:stop_key_pos]
            node_names.pop()
            #nodes.pop() Please fix this
            if len(nodes):
                parent_node = nodes[-1]
        else:
            elem_text = html_text[start_key_pos + 1:html_text.find("/")]
            elem_parts = elem_text.split(" ")
            id_name = None
            class_name = None
            for elem in elem_parts:
                if elem.find("=") == -1:
                    node_name = elem
                if elem.find("class") != -1:
                    class_name = elem
                if elem.find("id") != -1:
                    id_name = elem
            node_names.append(node_name)
            node = ElementNode(node_name, id_name, class_name)
            G.add_node(node)
            if parent_node:
                G.add_edge(parent_node, node)
    else:
        elem_text = html_text[start_key_pos + 1:stop_key_pos]
        elem_parts = elem_text.split(" ")
        id_name = None
        class_name = None
        for elem in elem_parts:
            if elem.find("=") == -1:
                node_name = elem
            if elem.find("class") != -1:
                class_name = elem
            if elem.find("id") != -1:
                id_name = elem
        node = ElementNode(node_name, id_name, class_name)
        nodes.append(node)
        node_names.append(node_name)
        G.add_node(node)
        if parent_node:
            G.add_edge(parent_node, node)
        parent_node = node

    html_text = html_text[stop_key_pos + 1:]

plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()
