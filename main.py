#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:        androidApp.py
# Purpose:     Example Application for the Navigationdrawer
#              based on code from Licia Leanza
#
# Author:      Stefan Murawski
#
# Created:     24-01-2016
# -------------------------------------------------------------------------------

import kivy
from kivy.app import App
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionBar, ActionButton, ActionPrevious
from kivy.properties import ObjectProperty

__author__ = 'steveway'

# --------------------------------------------------------------------------
'''dictionary that contains the correspondance between items descriptions
and methods that actually implement the specific function and panels to be
shown instead of the first main_panel
'''
SidePanel_AppMenu = {'entry one': ['on_one', None],
                     'entry two': ['on_two', None],
                     'entry three': ['on_three', None],
                     }
id_AppMenu_METHOD = 0
id_AppMenu_PANEL = 1


RootApp = None


class SidePanel(BoxLayout):
    pass


class MenuItem(Button):
    def __init__(self, **kwargs):
        super(MenuItem, self).__init__( **kwargs)
        self.bind(on_press=self.menuitem_selected)

    def menuitem_selected(self, *args):
        print self.text, SidePanel_AppMenu[self.text], SidePanel_AppMenu[self.text][id_AppMenu_METHOD]
        function_to_call = SidePanel_AppMenu[self.text][id_AppMenu_METHOD]
        getattr(RootApp, function_to_call)()


class AppActionBar(ActionBar):
    pass


class ActionMenu(ActionPrevious):
    def menu(self):
        print 'ActionMenu'
        RootApp.toggle_sidepanel()


class ActionQuit(ActionButton):
    pass
    def menu(self):
        print 'App quit'
        RootApp.stop()


class MainPanel(BoxLayout):
    pass


class AppArea(FloatLayout):
    pass


class PageOne(FloatLayout):
    pass


class PageTwo(FloatLayout):
    pass


class PageThree(FloatLayout):
    pass


class AppButton(Button):
    button_name = ObjectProperty(None)

    def app_pushed(self):
        print self.text, 'button', self.button_name.state


class NavDrawer(NavigationDrawer):
    def __init__(self, **kwargs):
        super(NavDrawer, self).__init__( **kwargs)

    def close_sidepanel(self, animate=True):
        if self.state == 'open':
            if animate:
                self.anim_to_state('closed')
            else:
                self.state = 'closed'


class AndroidApp(App):

    def build(self):

        global RootApp
        RootApp = self

        # NavigationDrawer
        self.navigationdrawer = NavDrawer()

        # SidePanel
        side_panel = SidePanel()
        self.navigationdrawer.add_widget(side_panel)

        # MainPanel
        self.main_panel = MainPanel()

        self.navigationdrawer.anim_type = 'slide_above_anim'
        self.navigationdrawer.add_widget(self.main_panel)

        return self.navigationdrawer

    def toggle_sidepanel(self):
        self.navigationdrawer.toggle_state()

    def on_one(self):
        print 'one... exec'
        self._switch_main_page('entry one', PageOne)

    def on_two(self):
        print 'two... exec'
        self._switch_main_page('entry two', PageTwo)

    def on_three(self):
        print 'three... exec'
        self._switch_main_page('entry three',  PageThree)

    def _switch_main_page(self, key,  panel):
        self.navigationdrawer.toggle_state()
        if not SidePanel_AppMenu[key][id_AppMenu_PANEL]:
            SidePanel_AppMenu[key][id_AppMenu_PANEL] = panel()
        main_panel = SidePanel_AppMenu[key][id_AppMenu_PANEL]
        self.navigationdrawer.remove_widget(self.main_panel)    # Without this the main_panel
        self.navigationdrawer.add_widget(main_panel)            # will not update currently.
        self.main_panel = main_panel


if __name__ == '__main__':
    AndroidApp().run()
