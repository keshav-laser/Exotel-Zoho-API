import fitz
# from extract_images import get_images

def getMap(fstr):
    str1 = ""
    str2 = ""
    found = False
    for i in range(len(fstr)):
        if fstr[i]==":" and found==False:
            found = True
        elif found == False:
            str1 += fstr[i]
        else:
            str2 += fstr[i]
    return str1.strip(), str2.strip()

def get_final_str_from_block(page,bbox,final_result):
    current_bbox = bbox
    textpage = page.get_textpage(clip=current_bbox)
    dicts = textpage.extractDICT()
    # dicts = page.get_text(option="dict")
    # print(dicts)
    for block in dicts['blocks']:
        final_str = ""
        map_found = False
        for line in block['lines']:
            str1 = ""
            for span in line["spans"]:
                # print(span['size'])
                str1 += span["text"]
            final_str += str1
            # print(str1)
            mapped_str11, mapped_str12 = getMap(final_str)
            # print(final_str)
            if mapped_str12!="" and mapped_str11!="":
                map_found = True
                final_result += mapped_str11 + "," + mapped_str12 + "\n"
                final_str = ""
            # print(final_str)
            # print("line end")
        # print("block end")
        mapped_str1, mapped_str2 = getMap(final_str)
        # print(final_str)
        if mapped_str1!="":
            pre = ""
            if mapped_str2=="" and map_found==True:
                pre = "##"
            final_result += pre + mapped_str1 + "," + mapped_str2 + "\n"
    return final_result

def post_process_result(final_result):
    final_result = final_result.replace("\n##"," ")
    textList = final_result.split('\n')
    final_result = ""
    for textElem in textList:
        tempStr = textElem.replace(",","")
        if len(tempStr)!=0:
            final_result += textElem + "\n"
    return final_result
# for i in range(doc.page_count):
#     page = doc.load_page(i)
#     textpage = page.get_textpage()
#     dicts = textpage.extractDICT()
#     # dicts = page.get_text(option="dict")
#     # print(dicts)
#     for block in dicts['blocks']:
#         final_str = ""
#         map_found = False
#         for line in block['lines']:
#             str1 = ""
#             for span in line["spans"]:
#                 # print(span['size'])
#                 str1 += span["text"]
#             final_str += str1
#             # print(str1)
#             mapped_str11, mapped_str12 = getMap(final_str)
#             # print(final_str)
#             if mapped_str12!="" and mapped_str11!="":
#                 map_found = True
#                 final_result += mapped_str11 + "," + mapped_str12 + "\n"
#                 final_str = ""
#             # print(final_str)
#             # print("line end")
#         # print("block end")
#         mapped_str1, mapped_str2 = getMap(final_str)
#         # print(final_str)
#         if mapped_str1!="":
#             pre = ""
#             if mapped_str2=="" and map_found==True:
#                 pre = "##"
#             final_result += pre + mapped_str1 + "," + mapped_str2 + "\n"
#         # print(block)
#         # print()

# # print(final_result)
# print()


# final_result = ""
# for i in range(doc.page_count):
#     page = doc.load_page(i)
#     textpage = page.get_textpage()
#     dicts = textpage.extractDICT()
#     # print(dicts)
#     for block in dicts['blocks']:
#         final_str = ""
#         for line in block['lines']:
#             str1 = ""
#             for span in line["spans"]:
#                 # print(span['size'])
#                 str1 += span["text"]
#             final_str += str1
#         # print("block end")
#         mapped_str1, mapped_str2 = getMap(final_str)
#         # print(final_str)
#         if mapped_str1!="":
#             final_result += mapped_str1 + "," + mapped_str2 + "\n"
#         # print(block)
#         # print()

# print(final_result)

def get_final_str(filename):
    j = 0
    resultList = list()
    final_result = ""
    doc = fitz.open("input/"+filename, filetype="pdf")
    for i in range(doc.page_count):
        page = doc.load_page(i)
        tables = page.find_tables()
        used_blocks = []
        resultList = list()
        for table in tables:
            resultList.append(table.extract())
            used_blocks.append([table.bbox[1],table.bbox[3]])
            # page.draw_rect(rect=table.bbox, color=(1,0,0))
            # pix = page.get_pixmap()
            # pix.save("extra/page-"+str(j)+".png")
            # j+=1
        previous_y = 0
        max_x = page.bound().x1
        max_y = page.bound().y1
        k = 0
        for used_block in used_blocks:
            final_result = get_final_str_from_block(page,(0,previous_y,max_x,used_block[0]),final_result)
            previous_y = used_block[1]
            table = resultList[k]
            tableToString = ""
            for row in table:
                for i in range(len(row)):
                    if i!=len(row)-1:
                        tableToString += str(row[i])+","
                    else:
                        tableToString += str(row[i])+"\n"
            tableToString+="\n"
            final_result += tableToString
        if previous_y < max_y:
            final_result = get_final_str_from_block(page,(0,previous_y,max_x,max_y),final_result)
    return post_process_result(final_result)

def get_final_str_from_stream(response_content):
    j = 0
    resultList = list()
    final_result = ""
    doc = fitz.open(stream=response_content, filetype="pdf")
    for i in range(doc.page_count):
        page = doc.load_page(i)
        tables = page.find_tables()
        used_blocks = []
        resultList = list()
        for table in tables:
            resultList.append(table.extract())
            used_blocks.append([table.bbox[1],table.bbox[3]])
            # page.draw_rect(rect=table.bbox, color=(1,0,0))
            # pix = page.get_pixmap()
            # pix.save("extra/page-"+str(j)+".png")
            # j+=1
        previous_y = 0
        max_x = page.bound().x1
        max_y = page.bound().y1
        k = 0
        for used_block in used_blocks:
            final_result = get_final_str_from_block(page,(0,previous_y,max_x,used_block[0]),final_result)
            previous_y = used_block[1]
            table = resultList[k]
            tableToString = ""
            for row in table:
                for i in range(len(row)):
                    if i!=len(row)-1:
                        tableToString += str(row[i])+","
                    else:
                        tableToString += str(row[i])+"\n"
            tableToString+="\n"
            final_result += tableToString
        if previous_y < max_y:
            final_result = get_final_str_from_block(page,(0,previous_y,max_x,max_y),final_result)
    return post_process_result(final_result)

# directory = '/home/keshav.singhal/Downloads/API for call logs/input'
# for file in os.listdir(directory):
#     if file.endswith(".pdf"):
#         final_result = get_final_str(file)
#         outfile = "output1/"+file[:-3]+"csv"
#         outputfile = open(outfile, "w") 
#         outputfile.write(final_result)
#         outputfile.close() 