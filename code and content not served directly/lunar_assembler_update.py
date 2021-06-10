import requests
import os

os.chdir("../osm_to_svg_in_browser")

session = requests.Session()

response = session.get('https://raw.githubusercontent.com/matkoniecz/lunar_assembler/master/examples/general_high_zoom.html')
with open('index.html', 'w') as file:
    page_text = response.text
    replacable = """<div id="main_content_wrap" class="outer">"""
    new_content = """<div id="main_content_wrap" class="outer">
        <nav role='navigation' class="main-nav">
            <ul id="main-nav-list">
              <li>
                <a href="../index.html">
                  <div>
                    Home
                  </div>
                </a>
              </li>
              <li>
                <a href="../articles.html">
                  <div>
                    Articles
                  </div>
                </a>
              </li>
              <li>
                <a href="../recommendations.html">
                  <div>
                    Recommendations
                  </div>
                </a>
              </li>
              <li>
                <a href="../contact.html">
                  <div>
                    Contact
                  </div>
                </a>
              </li>
            </ul>
          </nav>"""
    if replacable not in page_text:
        print(page_text)
        print("==== ^ text ==========")
        print("======================")
        print("==== v replacable ====")
        print(replacable)
        raise "text does not contain searched element"
    page_text = page_text.replace(replacable, new_content)
    file.write(page_text)

response = session.get('https://raw.githubusercontent.com/matkoniecz/lunar_assembler/master/examples/lunar_assembler.dist.js')
with open('lunar_assembler.dist.js', 'w') as file:
    file.write(response.text)

response = session.get('https://raw.githubusercontent.com/matkoniecz/lunar_assembler/master/examples/lunar_assembler.dist.css')
with open('lunar_assembler.dist.css', 'w') as file:
    file.write(response.text)

response = session.get('https://raw.githubusercontent.com/matkoniecz/lunar_assembler/master/examples/lunar_assembler_in_action.gif')
with open('lunar_assembler_in_action.gif', 'wb') as file:
    file.write(response.content)

response = session.get('https://raw.githubusercontent.com/matkoniecz/lunar_assembler/master/examples/general_high_zoom_map_style.js')
with open('general_high_zoom_map_style.js', 'w') as file:
    file.write(response.text)

