import json
import streamlit as st
from code_editor import code_editor

html_style_string = '''<style>
@media (min-width: 576px)
section div.block-container {
  padding-left: 20rem;
}
section div.block-container {
  padding-left: 4rem;
  padding-right: 4rem;
  max-width: 80rem;
}  
.floating-side-bar {
    display: flex;
    flex-direction: column;
    position: fixed;
    margin-top: 2rem;
    margin-left: 2.75rem;
    margin-right: 2.75rem;
}
.flt-bar-hd {
    color: #5e6572;
    margin: 1rem 0.1rem 0 0;
}
.floating-side-bar a {
    color: #b3b8c2;

}
.floating-side-bar a:hover {

}
.floating-side-bar a.l2 {

}
</style>'''

st.markdown(html_style_string, unsafe_allow_html=True)

# Opening JSON file
# You can also just use a dictionary but with files (JSON or text for example),
# its easier to transfer or use in multiple projects
with open('streamlit-code-editor/docs/pages/resources/example_custom_buttons_bar_adj.json') as json_button_file:
    custom_buttons_alt = json.load(json_button_file)

with open('streamlit-code-editor/docs/pages/resources/example_custom_buttons_set.json') as json_button_file:
    custom_buttons = json.load(json_button_file)

# Load Info bar CSS from JSON file
with open('streamlit-code-editor/docs/pages/resources/example_info_bar.json') as json_info_file:
    info_bar = json.load(json_info_file)

# Load Code Editor CSS from file
with open('streamlit-code-editor/docs/pages/resources/code_editor.scss') as css_file:
    css_text = css_file.read()

col1, col2 = st.columns([6,2])
with col1:
    st.markdown("## Advanced usage")
    st.markdown("This section covers the Code Editor's bi-directional capabilities, the addition of elements that add interactivity (such as buttons, info bar, and menu bar), and customization of more advanced features of the editor. Suffice it to say, there is a lot more you can do with the editor.")

    st.markdown("### Return value")
    st.markdown("The `code_editor` function returns a dictionary containing the text/code contents of the editor as well as other usefull info. You might expect the `code_editor` function to return its contents after every edit but this is not the case. The decision was made from the start to avoid doing this because it would have been detrimental to the user experience. Communicating back to the streamlit script results in a re-run of the script which can interupt user interactions with the component and/or delay its response. Even when the resulting delay between keystrokes is small, it will still noticeable impact the user experience. Instead, `code_editor` communicates back to the script (returns a dictionary containing the contents and more) when it is told to execute a command that does so. Code Editor components have a set of built-in commands, a few of which tell it to send back/return information to the script. There are a few ways the user can tell the editor to execute these commands and commands in general with the main way being through custom buttons.")

    st.markdown("### Custom buttons")
    st.markdown("Adding buttons is easy. You can add a button by passing a dictionary to the `custom_buttons` argument of the `code_editor` function.")

    custom_button_code ='''# add a button with text: 'Copy'\ncustom_btns = [{"name": "Copy"}]\nresponse_dict = code_editor(your_code_string, buttons=custom_btns)'''
    custom_button_code_show ='''[{"name": "Copy", "hasText": True}]'''
    custom_button_code_show_always ='''[{"name": "Copy", "hasText": True, "alwaysOn": True,}]'''
    custom_button_code_show_always_right ='''[{
  "name": "Copy",
  "hasText": True,
  "alwaysOn": True,
  "style": {"top": "0.46rem", "right": "0.4rem"}
}]'''
    btn_show_always_right_icon ='''[{
  "name": "Copy",
  "feather": "Copy",
  "alwaysOn": True,
  "style": {"top": "0.46rem", "right": "0.4rem"}
}]'''

    btn_show_always_right_icon_cmd ='''[{
  "name": "Copy",
  "feather": "Copy",
  "alwaysOn": True,
  "commands": ["copyAll"],
  "style": {"top": "0.46rem", "right": "0.4rem"}
}]'''

    response_custom_button = code_editor(custom_button_code, lang="python", buttons=[{"name": "Copy"}])
    st.markdown("Although you cant see it yet, a button has been added to the top left of the editor above. The only required attribute to add a button is the `name` attribute containing a string. The `name` attribute should contain the text that will be displayed on the button. The name attribute is also used in the id of the HTML button element so make sure it is unique. You can put any assortment of characters in the name attribute including spaces.")
    st.markdown("To show the text we have to set the `hasText` attribute to `True`.")
    response_custom_button_show = code_editor(custom_button_code_show, lang="python", buttons=[{"name": "Copy", "hasText": True}])
    st.markdown("The result is that a button with the text 'Copy' that is still invisible! But, what has changed here is that the button's text now becomes visible if you hover over the button (which is still in the top left corner). To get it to be always visible, we can set the alwaysOn attribute to True.")
    response_custom_button_show_always = code_editor(custom_button_code_show_always, lang="python", buttons=[{"name": "Copy", "hasText": True, "alwaysOn": True}])
    st.markdown("Now that the button is always visible, it becomes easier to see that its placement in this example is not ideal. To position a custom button, you can use the `style` attribute. This attribute sets the buttons element's [style property](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style). By default, custom buttons have their CSS postion property set to absolute so that they can be positioned anywhere (inside the iframe containing the Code Editor component) easily.")
    response_btn_show_always_right = code_editor(custom_button_code_show_always_right, lang="python", buttons=[{"name": "Copy", "hasText": True, "alwaysOn": True, "style": {"top": "0.46rem", "right": "0.4rem"}}])
    st.markdown("What if, instead of text, you want the button to have an icon like Streamlit's code block element's copy button? Code Editor allows you add any [Feather](https://feathericons.com/) icon to a custom button. To do so, set the `feather` attribute to the name of the icon you want to use. Make sure that the name of the icon is formatted: the first letter of each word separated with a dash is capitalized and the dash is removed. For example, 'alert-circle' becomes 'AlertCircle'. If we just want to show the icon, we can remove the text by removing the `hasText` attribute or setting it to `False`.")
    response_btn_show_always_right_icon = code_editor(btn_show_always_right_icon, lang="python", buttons=[{"name": "Copy", "feather": "Copy", "alwaysOn": True, "style": {"top": "0.46rem", "right": "0.4rem"}}])
    st.markdown("There is still one major issue with the button. It does not do anything. To make the button do something, we have to give it a list of commands we want Code Editor to execute when the button is clicked. We can do this by giving the `commands` attribute a list of the names of the commands we want executed. You can find a list of the built-in commands [here](https://github.com/bouzidanas/streamlit.io/blob/dev/streamlit-code-editor/code_editor/frontend/docs/commands.js).")
    response_btn_show_always_right_icon_cmd = code_editor(btn_show_always_right_icon_cmd, lang="python", buttons=[{"name": "Copy", "feather": "Copy", "alwaysOn": True, "commands": ["copyAll"], "style": {"top": "0.46rem", "right": "0.4rem"}}])
    st.markdown("The 'copyAll' command simply copies the entire contents of the editor to the clipboard.")

    st.markdown("For reference, here is the list of button attributes:")

    btn_attr_dict = r'''{
  "name":           ,# string (required) 
  "feather":        ,# string
  "iconSize":       ,# integer number
  "primary":        ,# boolean
  "hasText":        ,# boolean
  "showWithIcon":   ,# boolean
  "alwaysOn":       ,# boolean 
  "style":          ,# dictionary
  "theme":          ,# dictionary 
  "class":          ,# string
  "classToggle":    ,# string
  "commands":       ,# list
  "toggledCommands":,# list
  "bindKey":        ,# {win: string, mac: string}
}'''
    st.code(btn_attr_dict, language="python")

    st.markdown("#### Response commands")
    st.markdown("Among the commands (that can be given to be executed when a button is clicked) are special commands called 'response commands' which call Streamlit's `setComponentValue` function to return a dictionary to the script. For example, the 'submit' command sends the following dictionary to the streamlit script as the return value of the `code_editor` function (corresponding to the Code Editor that executed the command):")

    btn_submit_return = '''{
  "id": "unique-id", 
  "type": "submit",
  "lang": "python",
  "text": "the code in the editor",
  "cursor": {"row": 0, "column": 0},
}'''
    st.code(btn_submit_return, language="python")

    st.info("**Note:** The `id` attribute is a unique time-based id generated for each call of `setComponentValue` and thus should be different each time the Code Editor communicates back to Streamlit.")
    st.success("**Tip:** Setting the `key` argument of the `code_editor` function to a fixed value will preserve the Code Editor instance and prevent it from being recreated everytime the streamlit script is rerun. This results in the editor being more stable in appearance and behavior. However! This also means that the editor will not reset the response dictionary! The response dictionary will maintain the same values through reruns until the next response command is called! Remember, when a response command is called, the 'id' value changes to a new unique one.")

    st.markdown("#### Demo")
    st.markdown("The following is an example dictionary that adds multiple buttons, some that execute single commands including response commands and some that execute multiple commands. The buttons are also positioned differently and have different features turned on or off.")

    btns_demo = '''[
 {
   "name": "Copy",
   "feather": "Copy",
   "hasText": True,
   "alwaysOn": True,
   "commands": ["copyAll"],
   "style": {"top": "0.46rem", "right": "0.4rem"}
 },
 {
   "name": "Shortcuts",
   "feather": "Type",
   "class": "shortcuts-button",
   "hasText": True,
   "commands": ["toggleKeyboardShortcuts"],
   "style": {"bottom": "calc(50% + 1.75rem)", "right": "0.4rem"}
 },
 {
   "name": "Collapse",
   "feather": "Minimize2",
   "hasText": True,
   "commands": ["selectall",
                "toggleSplitSelectionIntoLines",
                "gotolinestart",
                "gotolinestart",
                "backspace"],
   "style": {"bottom": "calc(50% - 1.25rem)", "right": "0.4rem"}
 },
 {
   "name": "Save",
   "feather": "Save",
   "hasText": True,
   "commands": ["save-state", ["response","saved"]],
   "response": "saved",
   "style": {"bottom": "calc(50% - 4.25rem)", "right": "0.4rem"}
 },
 {
   "name": "Run",
   "feather": "Play",
   "primary": True,
   "hasText": True,
   "showWithIcon": True,
   "commands": ["submit"],
   "style": {"bottom": "0.44rem", "right": "0.4rem"}
 },
 {
   "name": "Command",
   "feather": "Terminal",
   "primary": True,
   "hasText": True,
   "commands": ["openCommandPallete"],
   "style": {"bottom": "3.5rem", "right": "0.4rem"}
 }
]'''

    response_btns_demo = code_editor(btns_demo, lang="python", height=20, buttons=custom_buttons)
    st.markdown("Something you might've noticed is that the buttons on the bottom right get highlighted in a different color when the mouse is hovered over them. This is because the `primary` attribute is set to `True` for those buttons. This attribute tells Code Editor to get the color from the 'primary' config option (in the theme section of the Streamlit config file).")
    st.info("**Note:** Some commands like 'response' take an argument. This argument may be a string, a number, or a dictionary. In the case of the 'response' command, the argument is a string. To add a command that takes an argument to the `commands` attribute, instead of a string with the name of the command, you add a list of two elements to the commands list. The first element of this inner list should be a string containing the name of the command and the second element should be the argument (string|number|dictionary)")
    st.success("**Tip:** For better reusability, you can store the buttons in a file (like a JSON file) and then load the buttons from the file. This way, you can easily reuse buttons you have created for one Streamlit app in another. A side benefit is that you can change the buttons without having to change the code.")

    st.markdown("### Info bar")
    st.markdown("The info bar is a component within Code Editor that can be used to display information. Adding one is similar to adding a button. You pass a dictionary to the `info` argument of the `code_editor` function. The dictionary should have the following attributes:")

    info_attr_dict = '''{
  "name":    ,# string
  "css":     ,# string
  "style":   ,# dictionary
  "info":    ,# Array of dictionaries
}'''
    st.code(info_attr_dict, language="python")

    st.markdown("Example: Info bar with a single info item")
    info_ex_dict = """# css to inject related to info bar
css_string = \'''\nbackground-color: #bee1e5;\n\nbody > #root .ace-streamlit-dark~& {\n   background-color: #262830;\n}\n\n.ace-streamlit-dark~& span {\n   color: #fff;\n   opacity: 0.6;\n}\n\nspan {\n   color: #000;\n   opacity: 0.5;\n}\n\n.code_editor-info.message {\n   width: inherit;\n   margin-right: 75px;\n   order: 2;\n   text-align: center;\n   opacity: 0;\n   transition: opacity 0.7s ease-out;\n}\n\n.code_editor-info.message.show {\n   opacity: 0.6;\n}\n\n.ace-streamlit-dark~& .code_editor-info.message.show {\n   opacity: 0.5;\n}\n\'''
# create info bar dictionary
info_bar = {
  "name": "language info",
  "css": css_string,
  "style": {
            "order": "1",
            "display": "flex",
            "flexDirection": "row",
            "alignItems": "center",
            "width": "100%",
            "height": "2.5rem",
            "padding": "0rem 0.75rem",
            "borderRadius": "8px 8px 0px 0px",
            "zIndex": "9993"
           },
  "info": [{
            "name": "python",
            "style": {"width": "100px"}
           }]
}
# add info bar to code editor
response_dict = code_editor(your_code_string, lang="python", height=20, info=info_bar)"""
    response_info_ex = code_editor(info_ex_dict, lang="python", height=20, info=info_bar)
    st.markdown("There is a lot going on here with css and style that will be covered in the next section. For now, consider the `info` attribute. To add info items to the info bar, you add a dictionary to the list given to the `info` attribute. An info item dictionary can have the following attributes:")

    info_item_attr_dict = '''{
  "name":    ,# string containing displayed text (required)
  "class":   ,# string
  "style":   ,# dictionary
  "theme":   ,# dictionary
}'''

    st.code(info_item_attr_dict, language="python")

    st.markdown("#### Info message")
    st.markdown("When you add an info bar with at least one info item to the code editor, an additional, special info item is added to the bar that is specifically setup to display text sent to it via the 'infoMessage' command. ")

    code_btns_info = '''# create copy button with 'infoMessage' command
  custom_btns = [{
      "name": "Copy",
      "feather": "Copy",
      "hasText": True,
      "alwaysOn": True,
      "commands": ["copyAll", 
                   ["infoMessage", 
                    {
                     "text":"Copied to clipboard!",
                     "timeout": 2500, 
                     "classToggle": "show"
                    }
                   ]
                  ],
      "style": {"right": "0.4rem"}
    }]
  # add button and previous info bar to code editor
  response_dict = code_editor(your_code_string, lang="python", height=20, info=info_bar, buttons=custom_btns)
  '''

    response_btn_info_msg = code_editor(code_btns_info, lang="python", height=20, info=info_bar, buttons=[{
        "name": "Copy",
        "feather": "Copy",
        "hasText": True,
        "alwaysOn": True,
        "commands": ["copyAll", ["infoMessage", {"text":"Copied to clipboard!", "timeout": 2500, "classToggle": "show"}]],
        "style": {"right": "0.4rem"}
      }])
    
    st.markdown("### Commands")
    st.markdown("There are two types of commands that fall under two categories. The two types are the commands that dont take any arguments and the ones that do. To determine if a command takes an argument or not and what argument it takes, see the list of [built-in commands](https://github.com/bouzidanas/streamlit.io/blob/dev/streamlit-code-editor/code_editor/frontend/docs/commands.js). For example:")
    st.code('''
{
    name: "centerselection",
    description: "Center selection",
    bindKey: bindKey(null, "Ctrl-L"),
    exec: function (editor) { editor.centerSelection(); },
    readOnly: true
}, 
{
    name: "gotoline",
    description: "Go to line...",
    bindKey: bindKey("Ctrl-L", "Command-L"),
    exec: function (editor, line) {
        if (typeof line === "number" && !isNaN(line))
            editor.gotoLine(line);
        editor.prompt({ $type: "gotoLine" });
    },
    readOnly: true
}''', language="javascript")
    st.markdown("If the `exec` attribute of a command contains a function that only takes `editor` as the argument, then that means the command requires no arguments from the user (the `editor` argument is internally provided by the editor itself). If the `exec` function takes additional arguments, then the user must provide those. Look to the following code block to determine the nature of the argument(s) you must provide.")
    st.markdown("The two categories of commands are the ones that come built into the inner Ace Editor and the ones added by Code Editor. The [built-in commands](https://github.com/bouzidanas/streamlit.io/blob/dev/streamlit-code-editor/code_editor/frontend/docs/commands.js) list contains both starting with the Ace Editor commands.")
    st.info("**Note:** Some commands have default keybindings. The `bindKey` property gives the keybinding for a command in the command list.")
    st.markdown("As explained in the previous sections, buttons added to Code Editor are able to do things thanks to commands. If you provide a list containing the names of the commands you want executed in sequence to the `commands` attribute of a button, then those commands will be executed when the button is clicked. An alternate list of commands can be provided to the `toggledCommands` attribute. These commands will be executed when the button is clicked while it is in the toggled state. This allows the buttons to do two different things depending on state (think on/off togglable buttons).")
    st.info("**Note:** Elements of command lists (in custom button dictionaries) must either be strings containing the name of a command or a list of elements starting with the name of the command followed by the argument to pass to the command for commands that take arguments.")
    st.info("**Note:** Button command lists can contain as little as one command (list of one command name string) or as many as you want. The commands will be executed in the order they are given.")
    st.info("**Note:** A command is created for every button that is added to Code Editor that allows the user to execute the button's commands without having to click the button. This can be useful in some circumstances.")
    st.warning("This section is incomplete. Please check back later.", icon="⚠️")

    st.markdown("### Menu bar")
    st.markdown("The menu bar is another component within Code Editor that can be used to add a menu. Adding one is similar to adding the info bar. ")
    st.warning("This section is incomplete. Please check back later.", icon="⚠️")

    st.markdown("### Overlays")
    st.warning("This section is incomplete. Please check back later.", icon="⚠️")

    st.markdown("### Keybindings and snippets")
    st.warning("This section is incomplete. Please check back later.", icon="⚠️")

floating_side_bar = '''
<div class="floating-side-bar">
    <span class="flt-bar-hd"> CONTENTS </span>
    <a href="#advanced-usage">Advanced usage</a>
    <a class="l2" href="#return-value">Return value</a>
    <a class="l2" href="#custom-buttons">Custom buttons</a>
    <a class="l3" href="#response-commands">Response commands</a>
    <a class="l3" href="#demo">Demo</a>
    <a class="l2" href="#info-bar">Info bar</a>
    <a class="l3" href="#info-message">Info message</a>
    <a class="l2" href="#menu-bar">Menu bar</a>
    <a class="l2" href="#overlays">Overlays</a>
    <a class="l2" href="#commands">Commands</a>
    <a class="l2" href="#keybindings-and-snippets">Keybindings and snippets</a>
    <span class="flt-bar-hd"> LINKS </span>
    <a href="https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style">style property</a>
    <a href="https://feathericons.com/">Feather</a>
    <a href="https://github.com/bouzidanas/streamlit.io/blob/dev/streamlit-code-editor/code_editor/frontend/docs/commands.js">built-in commands</a>
</div>
'''

with col2:
    st.markdown(floating_side_bar, unsafe_allow_html=True)