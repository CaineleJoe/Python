def camelToSnake(camel):
    snake=""
    for i in camel:
        if i.isupper() and snake:
            snake=snake+"_"+i.lower()
        else:
            if(snake):
                snake=snake+i.lower()
            else:
                snake=snake+i

    return snake
camel=input("String")
print(camelToSnake(camel))