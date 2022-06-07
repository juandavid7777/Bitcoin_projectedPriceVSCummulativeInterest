def css_to_rgb(color_name, opacity):
    import webcolors
   
    r,g,b = webcolors.name_to_rgb(color_name)
    return "rgba(" + str(r) + "," + str(g) + "," + str(b) + "," + str(opacity)+")"