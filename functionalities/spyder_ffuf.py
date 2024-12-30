import subprocess
import re

wordlist = '/usr/share/wordlists/wfuzz/general/big.txt'

#pattern to seperate the output
pattern = r"(?P<path>\S+)\s+\[Status:\s*(?P<status>\d+),\s*Size:\s*(?P<size>\d+),\s*Words:\s*(?P<words>\d+),\s*Lines:\s*(?P<lines>\d+),\s*Duration:\s*(?P<duration>\d+ms)\]"

#defining the tree node
#class to create nodes and add childs
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
    def add_child(self, child):
        self.children.append(child)

#main spyder class
class spyder_ffuf:
    def __init__(self,wordlist,url,recursive):
        print('fuzzing....')
        self.wordlist = wordlist
        self.url = url
        self.recursive = recursive

    #fuzz directories for the given url and get a list of dictionaries
    def get_dirs_files(self):
        ffuf_results = subprocess.run(['ffuf','-u',self.url,'-w',self.wordlist],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
        data = ffuf_results.stdout
        data = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', data)

        # Extract and print each match as a dictionary
        matches = re.finditer(pattern, data)
        result_list = [match.groupdict() for match in matches]
        return result_list
    

    #convert the data from the node to json format
    #convert the tree to json data
    def tree_to_json(self,node, prefix="1"):
        if not node:
            return {}
        
        # Use the existing `data` from the node and add `subItems`
        node_data = node.data.copy()  # Ensure we don't modify the original data
        node_data["subItems"] = {}
        
        # Traverse children recursively with updated prefixes
        for i, child in enumerate(node.children, start=1):
            sub_prefix = f"{prefix}.{i}"
            # Add the result of the recursive call without nesting another prefix
            node_data["subItems"].update(self.tree_to_json(child, sub_prefix))
        
        return {prefix: node_data}

    #get height of tree
    def tree_height(self,node):
        if node is None:
            return 0
        if not node.children:
            return 1
        return 1 + max(self.tree_height(child) for child in node.children)
        
    #get nodes at a layer
    def get_nodes_at_layer(self,rootNode, layer):  
        # Initialize a queue for BFS
        queue = [(rootNode, 0)]  # (node, current_layer)
        result = []
        
        while queue:
            current_node, current_layer = queue.pop(0)
            
            # If the current layer matches the desired layer, add to result
            if current_layer == layer:
                result.append(current_node)
            
            # If we've passed the desired layer, stop processing further layers
            if current_layer > layer:
                break
            
            # Add children to the queue with their layer incremented
            for child in current_node.children:
                queue.append((child, current_layer + 1))
        
        return result
    
    def manager(self):
        #initialize a root node
        root = TreeNode({'path':self.url})
        height = 0

        #till out tree's height doesnt reach the recursion value set by the user
        while height<=self.recursive:
            print(f'Layer:{height}')
            for el in self.get_nodes_at_layer(root,height):
                fuzz_results = get_fuzz_results(el.data['path']+ '/',wordlist)
                for f in fuzz_results:
                    if f['status'] != '403':
                        del f['words']
                        del f['lines']
                        f['label']=f['path']
                        f['path']=el.data['path']+'/'+f['path']
                        
                        el.add_child(TreeNode(f))
                print(fuzz_results) #list of dics
                print(el.data)
                
            height+=1

        return root



def get_fuzz_results(link,wordlist):
        urlToFuzz = link + '/FUZZ'
        fuzzer = spyder_ffuf(wordlist,urlToFuzz,recursive=1)
        result = fuzzer.get_dirs_files() #a list of all fuzz results
        
        return result