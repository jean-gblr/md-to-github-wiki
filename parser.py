import re
import sys
import os

regex_toc_line = "- \[(.*)\]\(#(T-.*) .*\)"
regex_toc_content = "<a name='.*>([^€]+?)<a name"
regex_toc_link = "\#T.*'"

class MdChunk():
    def __init__(self, page_name, page_tag, page_content):
        self.page_name = page_name
        self.page_tag = page_tag
        self.page_content = page_content

class DividePages(object):
    def __init__(self):
        #creation de la liste de chunk
        self.md_chunk_list = []
        self.toc_content = ""
        self.args = []

        #recuperation des arguments
        for x in sys.argv:
            self.args.append(x)

        #check if number of args = 3 else stop script
        if(len(self.args) != 4):
            print('\n/!\\ You need two arguments. /!\\')
            print('python3 .\\parser.py [yourfile.md] [outputpath] [github_wiki_link]\n')
            print('Exemple : python3 .\\parser.py .\\File.md c:\\Users\\Jean\\Documents\\md-to-github-wiki.wiki https://github.com/jean/md-to-github-wiki/wiki/')
            sys.exit()

        #ouverture du fichier
        self.file_name = self.args[1]
        #lire tout le fichier
        file = open(self.file_name, mode='r')
        content = file.read()
        self.file_content = content
        #self.file_content = content.split('\n')
        # close the file
        file.close()

    def parse_and_fill_chunks(self):
        #init le parseur regex
        #find les lignes avec name et #T
        res = re.findall(regex_toc_line, self.file_content)
        self.toc_content = re.search(regex_toc_content, self.file_content).group(1)
        
        for item in res:
            #creation des mdchunk avec page_name
            regex_content = "(<a name='" + item[1] + ".*<\/a>[^€]+?)<a name='T"
            
            content = re.search(regex_content, str(self.file_content), re.MULTILINE)
            if content is not None:
                self.md_chunk_list.append(MdChunk(item[0], item[1], content.group(1)))
    
    

    def rewrite_links(self):
        regex_rewrite = "#T.*-"
        self.toc_content = re.sub(regex_rewrite, self.args[3], self.toc_content)
        toc_lines = self.toc_content.split("\n")
        link = ""
        new_toc_content = ""
        for line in toc_lines:
            #print(line)
            res = re.search("(https.*) ", line)
            #enters if if finds https
            if res is not None:
                link = res.group(1)
            #did not find https
            else:
                pos = re.search("#[A-Z]", line)
                if pos is not None:
                    pos_int = pos.start()
                    if pos_int > 0:
                        line = line[ : pos_int] + link + line[pos_int : ]
            new_toc_content += line + '\n'
        self.toc_content = new_toc_content
    
    def write_files(self):
        directory = '{}\\'.format(self.args[2])
        home_file_name = directory + "Home.md"
        os.makedirs(os.path.dirname(home_file_name), exist_ok=True)
        with open(home_file_name, "w") as f:
            f.write(self.toc_content)
        for chunk in self.md_chunk_list:
            filename = directory + chunk.page_name + ".md"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                f.write(chunk.page_content)

    def test(self):
        print(self.file_content)

    def test_chunk_name(self):
        for chunk in self.md_chunk_list:
            print("name->"+chunk.page_name+"//// tag->"+chunk.page_tag)

    def test_chunk_content(self):
        chunk = self.md_chunk_list.pop(0)
        print(chunk.page_content)

exec = DividePages()
#exec.test()
exec.parse_and_fill_chunks()
exec.rewrite_links()
#exec.test_chunk_name()
#exec.test_chunk_content()
exec.write_files()
