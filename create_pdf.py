import fitz

doc = fitz.open()
page = doc.new_page()
page.insert_text((50, 50), "Table of Contents")
page.insert_text((50, 70), "1. Introduction ..................... 2")
page.insert_text((50, 90), "2. Methodology ...................... 3")
page.insert_text((50, 110), "3. Results .......................... 4")

page2 = doc.new_page()
page2.insert_text((50, 50), "1. Introduction")
page2.insert_text((50, 70), "This is the intro.")

page3 = doc.new_page()
page3.insert_text((50, 50), "2. Methodology")
page3.insert_text((50, 70), "This is the method.")

page4 = doc.new_page()
page4.insert_text((50, 50), "3. Results")
page4.insert_text((50, 70), "These are the results.")
    
# Add metadata TOC
# [lvl, title, page_num]
doc.set_toc([
    [1, "Introduction", 2],
    [1, "Methodology", 3],
    [1, "Results", 4]
])

doc.save("data/example_toc.pdf")
print("Created data/example_toc.pdf")
