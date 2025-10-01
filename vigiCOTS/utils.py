
def search_exploits(cve_id):
    try:
        search_id = cve_id[4:]
        result = subprocess.run(['searchsploit', '--cve', search_id], capture_output=True, text=True)
        if 'Exploits: No Results' in result.stdout:
            return("Pas d'exploit trouvé")
        else:
            results = result.stdout.split('-\n')[2:-1]
            
            exploits_list = '<ul>\n'
            for r in results:
                cleanedR = r.split('\n')[0]
                title, path = cleanedR.split("|")
                exploit = "<li>" + title.rstrip() + ", path=" + path + "</li>\n"
                exploits_list += exploit
            return exploits_list + "</ul>"
    except Exception as e:
        print("Ah shiiiiiit here we go again !\nError: %s", str(e))
        return str(e)
