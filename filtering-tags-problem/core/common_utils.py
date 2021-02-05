def multiply_list(list, n):
    if list[0] == "":
        return []
    
    if n == 0:
        return list
    
    return [ele + "," for ele in list for _ in range(n)]

#def create_filter_expression1(options):
#    filter_expressions = []

#    filter_list_len = len(filter_expressions)
#    if options["container"]:
#        container_list = options["container"].strip().split(",")
#        for container in container_list:
#            filter_expressions.append("@container = \'" + container.strip() + "\'")

    
#    filter_list_len = len(filter_expressions)
#    if options["name_starts_with"]:
#        name_filter_list = options["name_starts_with"].strip().split(",")
#        name_filter_count = len(name_filter_list)

#        filter_expressions = multiply_list(filter_expressions, name_filter_count)
#        for name_filter in name_filter_list:
#            #filter_expressions[i] = filter_expressions[i] + "@name=\"" + name_filter.strip() + "\"" for i in rangefilter_list_len)

#        filter_list_len = len(filter_expressions)

#    return filter_expressions



def create_filter_expression(options):
    filter_expressions = ""

    if options["container"]:
        filter_expressions = "@container='" + options["container"].strip() + "',"
       
#    if options["name_starts_with"]:
#        filter_expressions += "\"Name\"='" + options["name_starts_with"].strip() + "'"
        
    
    return filter_expressions



if __name__ == "__main__":
    options = {}
    #options["container"] = "con1, con2, con3"
    #options["name_starts_with"] = "abc, def, xyz"

    options["container"] = "con1"
    options["name_starts_with"] = "abc"


    expr_list = create_filter_expression(options)
    for expr in expr_list:
        print(expr)