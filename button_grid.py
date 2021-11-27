import wx
import random
import threading
import time
# TODO: Make an opening animation
# TODO: Clean up the fucking code
# TODO: Make the program do something when the answer is correct
# TODO: Play with the background color
# TODO: Make sure these are the correct ranges before you full send


class ComboButton(wx.Button):

    clicked = False
    status = -1





class MyPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.PREFLOP = 701
        self.VISID = 702
        self.starting_hands = [['AA', 'AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s'],
                                ['AKo','KK', 'KQs', 'KJs', 'KTs', 'K9s', 'K8s', 'K7s', 'K6s', 'K5s', 'K4s',  'K3s', 'K2s'],
                                ['AQo', 'KQo', 'QQ', 'QJs', 'QTs', 'Q9s', 'Q8s', 'Q7s', 'Q6s', 'Q5s', 'Q4s', 'Q3s', 'Q2s'],
                                ['AJo', 'KJo', 'QJo', 'JJ', 'JTs', 'J9s', 'J8s', 'J7s', 'J6s', 'J5s', 'J4s', 'J3s', 'J2s'],
                                ['ATo', 'KTo', 'QTo', 'JTo', 'TT', 'T9s', 'T8s', 'T7s', 'T6s', 'T5s', 'T4s', 'T3s', 'T2s'],
                                ['A9o', 'K9o', 'Q9o', 'J9o', 'T9o', '99', '98s', '97s', '96s', '95s', '94s', '93s', '92s'],
                                ['A8o', 'K8o', 'Q8o', 'J8o', 'T8o', '98o', '88', '87s', '86s', '85s', '84s', '83s', '82s'],
                                ['A7o', 'K7o', 'Q7o', 'J7o', 'T7o', '97o', '87o', '77', '76s', '75s', '74s', '73s', '72s'],
                                ['A6o', 'K6o', 'Q6o', 'J6o', 'T6o', '96o', '86o', '76o', '66', '65s', '64s', '63s', '62s'],
                                ['A5o', 'K5o', 'Q5o', 'J5o', 'T5o', '95o', '85o', '75o', '65o', '55', '54s', '53s', '52s'],
                                ['A4o', 'K4o', 'Q4o', 'J4o', 'T4o', '94o', '84o', '74o', '64o', '54o', '44', '43s', '42s'],
                                ['A3o', 'K3o', 'Q3o', 'J3o', 'T3o', '93o', '83o', '73o', '63o', '53o', '43o', '33', '32s'],
                                ['A2o', 'K2o', 'Q2o', 'J2o', 'T2o', '92o', '82o', '72o', '62o', '52o', '42o', '32o', '22']]
        self.questions = ["UTG Open", "MP Open", "CO Open", "BTN Open", "SB Open", "BB Vs UTG Raise", "BB Vs MP Raise",
                            "BB Vs CO Raise", "BB Vs BTN Raise", "BB Vs SB Raise", "SB Vs UTG Raise", "SB Vs MP Raise",
                            "SB Vs CO Raise", "SB Vs BTN Raise", "BTN Vs UTG Raise", "BTN Vs MP Raise", "BTN Vs CO Raise",
                            "CO Vs UTG Raise", "CO Vs MP Raise", "MP Vs UTG Raise", "SB Vs BB 3Bet", "BTN Vs BB 3Bet",
                            "BTN Vs SB 3Bet", "CO Vs BB 3Bet", "CO Vs SB 3Bet", "CO Vs BTN 3Bet", "MP Vs BB 3Bet",
                            "MP Vs SB 3Bet", "MP Vs BTN 3Bet", "MP Vs CO 3Bet", "UTG Vs BB 3Bet", "UTG Vs SB 3Bet",
                            "UTG Vs BTN 3Bet", "UTG Vs CO 3Bet", "UTG Vs MP 3Bet" ]
        self.solutions = {}
        self.buildSolutions()
        self.current_question = random.randint(0,len(self.questions)-1) #TODO: Possibly do some scheduling like in anki or at least a randomized/looped order
        # self.fold_color = (255, 0, 0, 255)
        self.incorrect_squares = {"Call": [], "Raise": []}
        self.call_color = (200, 61, 255, 255)
        self.raise_color = (116, 255, 61, 255)
        self.clear_color = (16, 81, 255, 255)
        self.mode = 2
        self.shift_down = False #Whether the shift key was pressed on the last button
        self.last_button_pressed = "AA"
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.range_and_cols = wx.BoxSizer(wx.VERTICAL)
        self.range_sizer = wx.GridSizer(rows=13, cols=13, hgap=0, vgap=0)
        self.training_mode = parent.PREFLOP

        self.squares = []
        for row in range(13):
            self.squares.append([ComboButton(self, label=self.starting_hands[row][i], size=(50,50)) for i in range(13)])
            for button in self.squares[row]:
                button.Bind(wx.EVT_BUTTON, self.on_button)
                button.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
                button.Bind(wx.EVT_KEY_UP, self.onKeyUp)
                self.startingColor(button)
                self.range_sizer.Add(button)

        self.row_fillers_sizer = wx.GridSizer(rows=14, cols=1, hgap=0, vgap=0)
        self.row_fillers = [ComboButton(self, label="<", size=(50,50)) for i in range(13)]
        for button in self.row_fillers:
            button.Bind(wx.EVT_BUTTON, self.fill_row)
            self.row_fillers_sizer.Add(button)
        self.enterButton = ComboButton(self, label="Etr", size=(50,50))
        self.enterButton.Bind(wx.EVT_BUTTON, self.on_enter)
        self.row_fillers_sizer.Add(self.enterButton)

        self.range_and_cols.Add(self.range_sizer)

        self.col_fillers_sizer = wx.GridSizer(rows=1, cols=13, hgap=0, vgap=0)
        self.col_fillers = [ComboButton(self, label="^", size=(50,50)) for i in range(13)]
        for button in self.col_fillers:
            button.Bind(wx.EVT_BUTTON, self.fill_col)
            self.col_fillers_sizer.Add(button)
        self.range_and_cols.Add(self.col_fillers_sizer)

        self.main_sizer.Add(self.range_and_cols)
        self.main_sizer.Add(self.row_fillers_sizer)


        self.options_sizer = wx.BoxSizer(wx.VERTICAL)
        # self.fold = wx.Button(self, label="Fold")
        # self.fold.SetBackgroundColour(self.fold_color)
        # self.fold.Bind(wx.EVT_BUTTON, self.on_fold)
        # self.options_sizer.Add(self.fold, proportion=1,
        #                 flag = wx.ALL | wx.CENTER | wx.EXPAND,
        #                 border=5)
        self.call = wx.Button(self, label="Call")
        self.call.SetBackgroundColour(self.call_color)
        self.call.Bind(wx.EVT_BUTTON, self.on_call)
        self.options_sizer.Add(self.call, proportion=1,
                        flag = wx.ALL | wx.CENTER | wx.EXPAND,
                        border=5)
        self.raised = wx.Button(self, label="Raise")
        self.raised.SetBackgroundColour(self.raise_color)
        self.raised.Bind(wx.EVT_BUTTON, self.on_raise)
        self.options_sizer.Add(self.raised, proportion=1,
                        flag = wx.ALL | wx.CENTER | wx.EXPAND,
                        border=5)
        self.clear = wx.Button(self, label="Clear")
        self.clear.SetBackgroundColour(self.clear_color)
        self.clear.Bind(wx.EVT_BUTTON, self.on_clear)
        self.options_sizer.Add(self.clear, proportion=1,
                        flag = wx.ALL | wx.CENTER | wx.EXPAND,
                        border=5)

        self.main_sizer.Add(self.options_sizer)

        self.question_text = wx.StaticText(self,-1, self.questions[self.current_question],
                                        size=(400, 800),
                                        style=wx.ALIGN_CENTER)

        self.font = self.question_text.GetFont()
        self.font.PointSize+=80
        self.question_text.SetFont(self.font)

        self.main_sizer.Add(self.question_text)
        self.SetSizer(self.main_sizer)

###########################################################################################################################################################################
    def preFlop(self, event):
        print("PREFLOP")

    def getButton(self, event_id): #Given an event ID, returns the card button associated with it
        for row in self.squares:
            for button in row:
                if button.Id == event_id:
                    return button  #At some point, you may have to return something other than the label

    def getRow(self, event_id): #returns an integer corresponding to the row to color
        for row in range(len(self.row_fillers)):
                if self.row_fillers[row].Id == event_id:
                    return row, self.row_fillers[row]

    def getCol(self, event_id): #returns an integer corresponding to the row to color
        for col in range(len(self.col_fillers)):
                if self.col_fillers[col].Id == event_id:
                    return col, self.row_fillers[col]

    def getCoords(self, label): #This function returns the coordinates in the matrix for a given label
        for row_index in range(13):
            for button_index in range(13):
                if self.squares[row_index][button_index].GetLabel() == label:
                    return (row_index, button_index)

    def calculateShiftRange(self, button): #This function takes a button and the global last_button_pressed and calculates cells in the shift range
        button_coords = self.getCoords(button.GetLabel())
        last_button_pressed_coords = self.getCoords(self.last_button_pressed)
        #At this point you have two coordinates (x, y) that represent (row, col)
        shift_range = []
        if button_coords == last_button_pressed_coords:
            return shift_range
        #Figure out which of the coordinates is farther to the left and higher
        if (button_coords[0] - last_button_pressed_coords[0])+(button_coords[1] - last_button_pressed_coords[1]) > 0: #regular rectangle
            for row in range(13):
                for col in range(13):
                    if (last_button_pressed_coords[0] <= row <= button_coords[0]) and (last_button_pressed_coords[1] <= col <= button_coords[1]):
                        shift_range.append(self.squares[row][col].GetLabel())
        else: #the shift-pressed button is to the upper left of the previous buttons
            for row in range(13):
                for col in range(13):
                    if (button_coords[0] <= row <= last_button_pressed_coords[0]) and (button_coords[1] <= col <= last_button_pressed_coords[1]):
                        shift_range.append(self.squares[row][col].GetLabel())
        return shift_range


    def on_button(self, event):
        button = self.getButton(event.Id)
        #print(button.GetLabel())
        if self.shift_down: #If the shift key was pressed in conjunction with the button
            #print("SHIFT DOWN") #TODO: This is still buggy but passable for now
            shift_range = self.calculateShiftRange(button) #This should be a list of cells to highlight
            print(shift_range)
            for row in self.squares:
                for btn in row:
                    if btn.GetLabel() in shift_range:
                        if self.mode == 1:
                            btn.SetBackgroundColour(self.call_color)
                            btn.clicked = True
                            btn.status = 1
                        elif self.mode == 2:
                            btn.SetBackgroundColour(self.raise_color)
                            btn.clicked = True
                            btn.status = 2
            self.last_button_pressed = button.GetLabel()
            #print("Last button pressed: ", self.last_button_pressed)
            return
                            #TODO: Clean up this code
        if button.clicked == True:
            self.startingColor(button) #THis makes the botton's color go away
            button.clicked = False
            button.status = -1
        else:
            if self.mode == 1:
                button.SetBackgroundColour(self.call_color)
                button.clicked = True
                button.status = 1
            elif self.mode == 2:
                button.SetBackgroundColour(self.raise_color)
                button.clicked = True
                button.status = 2
        self.last_button_pressed = button.GetLabel() #This allows us to determine the range of hands to select if shift were pressed
        print("Last button pressed: ", self.last_button_pressed)

    def onKeyDown(self, event):
        """
        If shift key is down, set class variable to True
        """
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SHIFT:
            self.shift_down = True
        event.Skip()

    #----------------------------------------------------------------------
    def onKeyUp(self, event):
        """
        If shift key is up, set class variable to False
        """
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SHIFT:
            self.shift_down = False
        event.Skip()

    # def on_fold(self, event):
    #     self.mode = 1

    def on_call(self, event):
        self.mode = 1

    def on_raise(self, event):
        self.mode = 2

    def on_clear(self, event):
        self.clearBoard()

    def fill_row(self, event):
        row_index, row_button = self.getRow(event.Id)
        if row_button.clicked == False: #Fill the whole row
            for button in self.squares[row_index]:
                if self.mode == 1:
                    if button.clicked == False:
                        button.SetBackgroundColour(self.call_color)
                        button.clicked = True
                        button.status = 1
                else:
                    if button.clicked == False:
                        button.SetBackgroundColour(self.raise_color)
                        button.clicked = True
                        button.status = 2
            row_button.clicked = True
        else: #Unfill the whole row
            for button in self.squares[row_index]:
                if button.status == self.mode:
                    self.startingColor(button)
                    button.clicked = False
                    button.status = -1
            row_button.clicked = False

    def fill_col(self, event):
        col_index, col_button = self.getCol(event.Id)
        if col_button.clicked == False: #Fill the whole row
            for button in [self.squares[i][col_index] for i in range(13)]:
                if self.mode == 1:
                    if button.clicked == False:
                        button.SetBackgroundColour(self.call_color)
                        button.clicked = True
                        button.status = 1
                else:
                    if button.clicked == False:
                        button.SetBackgroundColour(self.raise_color)
                        button.clicked = True
                        button.status = 2
            col_button.clicked = True
        else: #Unfill the whole row
            for button in [self.squares[i][col_index] for i in range(13)]:
                if button.status == self.mode:
                    self.startingColor(button) #THis makes the botton's color go away
                    button.clicked = False
                    button.status = -1
            col_button.clicked = False

            # TODO: Maybe keep a live update of the percent you have correct
            # TODO: Add a startup animation with the colors?
    def rangeConvert(self, handRange): #Takes a Flopzilla Handrange and turns it into a full list of hands MUST TAKE A STRING
        outputRange = []
        order = "AKQJT98765432"
        words = handRange.split(',')
        for word in words:
            elements = word.split('-')
            if len(elements) == 1:
                outputRange.append(elements[0]) #THis is if there is a single combo listed in the range_sizer
            else: #This is a standard AB-AC form
                if elements[0][0] == elements[0][1]: #If we're dealing with pairs
                    for i in range(order.index(elements[0][0]), order.index(elements[1][0])+1):
                        outputRange.append(order[i] + order[i])
                elif elements[0][2] == 's': #Dealing with a suited range
                    for i in range(order.index(elements[0][1]), order.index(elements[1][1])+1):
                        outputRange.append(elements[0][0] + order[i] + 's')
                elif elements[0][2] == 'o': #Dealing with an offsuit range
                    for i in range(order.index(elements[0][1]), order.index(elements[1][1])+1):
                        outputRange.append(elements[0][0] + order[i] + 'o')
        return outputRange

    def buildSolutions(self):
        with open("solutions.txt", "r") as f:
            for line in f:
                sections = line.split(":")
                #print(sections)
                raise_range = sections[1].split(" ")
                if len(raise_range) == 1:
                    raise_range = []
                else:
                    raise_range = self.rangeConvert(raise_range[1].strip())
                call_range = sections[2].split(" ")
                if len(call_range) == 1:
                    call_range = []
                else:
                    call_range = self.rangeConvert(call_range[1].strip())
                self.solutions[sections[0]] = {"Raise":sorted(raise_range), "Call":sorted(call_range) }
        #print(self.solutions)




    def getBoardStatus(self): #This gets the current pressed buttons using a dictionary of the form {Raise: [], Call:[]}
        status = {"Raise": [], "Call": []}
        for row in self.squares:
            for button in row:
                if button.status == 1:
                    status["Call"].append(button.GetLabel())
                elif button.status == 2:
                    status["Raise"].append(button.GetLabel())
        status["Raise"] = sorted(status["Raise"])
        status["Call"] = sorted(status["Call"])
        return status

    def clearBoard(self):
        for row in self.squares:
            for button in row:
                button.status = -1
                button.clicked = False
                self.startingColor(button)



    def on_enter(self, event): #Works!!!
        #if self.training_mode == self.PREFLOP:

        user_soln = self.getBoardStatus() #Dictionary containing what the user has entered so far
        #print("User")
        #print(user_soln)
        real_soln = self.solutions[self.questions[self.current_question]] #Actual answer
        #print("Real")
        #print(real_soln)
        if user_soln == real_soln:
            print("CORRECT")
            self.current_question = random.randint(0,len(self.questions)-1)
            self.question_text.SetLabel(self.questions[self.current_question])
            self.clearBoard()
        else: #Have it show temporarily the incorrect squares
            self.incorrect_squares = {"Call": [], "Raise": []}
            extra_user_calls = [x for x in user_soln["Call"] if x not in real_soln["Call"]]
            extra_user_raises = [x for x in user_soln["Raise"] if x not in real_soln["Raise"]]
            unclicked_real_calls = [x for x in real_soln["Call"] if x not in user_soln["Call"]]
            unclicked_real_raises = [x for x in real_soln["Raise"] if x not in user_soln["Raise"]]
            for x in extra_user_calls:
                self.incorrect_squares["Call"].append(x)
            for x in unclicked_real_calls:
                self.incorrect_squares["Call"].append(x)
            for x in extra_user_raises:
                self.incorrect_squares["Raise"].append(x)
            for x in unclicked_real_raises:
                self.incorrect_squares["Raise"].append(x)

            print(self.incorrect_squares)
            for row in self.squares:
                for button in row:
                    if button.GetLabel() in self.incorrect_squares["Call"] or button.GetLabel() in self.incorrect_squares["Raise"]:
                        button.SetBackgroundColour((255, 0,0,255))
            #time.sleep(0.1)
            x = threading.Thread(target=self.incorrectSoln, daemon=True)
            x.start()
            print("INCORRECT")

    def incorrectSoln(self):
        time.sleep(0.5)
        for row in self.squares:
            for button in row:
                if button.GetLabel() in self.incorrect_squares["Call"] or button.GetLabel() in self.incorrect_squares["Raise"]:
                    if button.clicked == True:
                        if button.status == 1:
                            button.SetBackgroundColour(self.call_color)
                        elif button.status == 2:
                            button.SetBackgroundColour(self.raise_color)
                    else:
                        self.startingColor(button)


    def startingColor(self, button):
        if 's' in button.GetLabel():
            button.SetBackgroundColour((255, 245, 187, 255))
        elif 'o' in button.GetLabel():
            button.SetBackgroundColour((255, 215, 205, 255))
        else:
            button.SetBackgroundColour((181, 230, 253, 255))




class MyFrame(wx.Frame):
    size = (1200,800)

    def __init__(self):
        super().__init__(None, title="Preflop Range Trainer", size=self.size)

        self.PREFLOP = 701
        self.VISID = 702
        self.panel = MyPanel(self)

        menuBar = wx.MenuBar()

        modeMenu = wx.Menu()
        preflop = wx.MenuItem(modeMenu, self.PREFLOP, text="Preflop Ranges", kind=wx.ITEM_NORMAL)
        modeMenu.Append(preflop)
        visID = wx.MenuItem(modeMenu, self.VISID, text="Vis ID", kind=wx.ITEM_NORMAL)
        modeMenu.Append(visID)

        menuBar.Append(modeMenu, "Mode")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.menuhandler)
        self.Show()

    def menuhandler(self, event):
        id = event.GetId()
        if id == self.PREFLOP:
            self.panel.training_mode = self.PREFLOP
        elif id == self.VISID:
            self.panel.training_mode = self.VISID


if __name__ == "__main__":
    app = wx.App(redirect=False)
    frame=MyFrame()
    app.MainLoop()
