from navutils.menu import register, Menu, AuthenticatedNode


def create_menu(name, nodes):
    menu = Menu(name)
    for node in nodes:
        menu.register(node)
    register(menu)


create_menu('main', [
    AuthenticatedNode(id='organisation', label='Organizacija', pattern_name='index', children=[
        AuthenticatedNode(id='volunteers', label='Savanoriai', pattern_name='volunteers_list'),
    ])
])
