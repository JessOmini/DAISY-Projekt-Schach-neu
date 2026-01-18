import numpy as np

class Piece:
    """
    Base class for pieces on the board. 
    
    A piece holds a reference to the board, its color and its currently located cell.
    In this class, you need to implement two methods, the "evaluate()" method and the "get_valid_cells()" method.
    """
    def __init__(self, board, white):
        """
        Constructor for a piece based on provided parameters

        :param board: Reference to the board this piece is placed on
        :type board: :ref:class:`board`
        """
        self.board = board
        self.white = white
        self.cell = None



    def is_white(self):
        """
        Returns whether this piece is white

        :return: True if the piece white, False otherwise
        """
        return self.white

    def can_enter_cell(self, cell):
        """
        Shortcut method to see if a cell on the board can be entered.
        Simply calls :py:meth:`piece_can_enter_cell <board.Board.piece_can_enter_cell>` from the current board class.

        :param cell: The cell to check for. Must be a unpackable (row, col) type.
        :return: True if the provided cell can enter, False otherwise
        """
        return self.board.piece_can_enter_cell(self, cell)

    def can_hit_on_cell(self, cell):
        """
        Shortcut method to see if this piece can hit another piece on a cell.
        Simply calls :py:meth:`piece_can_hit_on_cell <board.Board.piece_can_hit_on_cell>` from the current board class.

        :param cell: The cell to check for. Must be a unpackable (row, col) type.
        :return: True if the piece can hit on the provided cell, False otherwise
        """
        return self.board.piece_can_hit_on_cell(self, cell)

    def evaluate(self):
        """
        **TODO** Implement a meaningful numerical evaluation of this piece on the board.
        This evaluation happens independent of the color as later, values for white pieces will be added and values for black pieces will be substracted. 
        
        **HINT** Making this method *independent* of the pieces color is crucial to get a *symmetric* evaluation metric in the end.
         
        - The pure existance of this piece alone is worth some points. This will create an effect where the player with more pieces on the board will, in sum, get the most points assigned. 
        - Think of other criteria that would make this piece more valuable, e.g. movability or whether this piece can hit other pieces. Value them accordingly.
        
        :return: Return numerical score between -infinity and +infinity. Greater values indicate better evaluation result (more favorable).
        """
        # TODO: Implement
        values = {
            Pawn: 1.0,
            Knight: 3.0,
            Bishop: 3.0,
            Rook: 5.0,
            Queen: 100.0,
            King: 1000.0,
        }
        return values[type(self)]

    def get_valid_cells(self):
        """
        **TODO** Return a list of **valid** cells this piece can move into. 
        
        A cell is valid if 
          a) it is **reachable**. That is what the :py:meth:`get_reachable_cells` method is for and
          b) after a move into this cell the own king is not (or no longer) in check.

        **HINT**: Use the :py:meth:`get_reachable_cells` method of this piece to receive a list of reachable cells.
        Iterate through all of them and temporarily place the piece on this cell. Then check whether your own King (same color)
        is in check. Use the :py:meth:`is_king_check_cached` method to test for checks. If there is no check after this move, add
        this cell to the list of valid cells. After every move, restore the original board configuration. 
        
        To temporarily move a piece into a new cell, first store its old position (self.cell) in a local variable. 
        The target cell might have another piece already placed on it. 
        Use :py:meth:`get_cell <board.BoardBase.get_cell>` to retrieve that piece (or None if there was none) and store it as well. 
        Then call :py:meth:`set_cell <board.BoardBase.set_cell>` to place this piece on the target cell and test for any checks given. 
        After this, restore the original configuration by placing this piece back into its old position (call :py:meth:`set_cell <board.BoardBase.set_cell>` again)
        and place the previous piece also back into its cell. 
        
        :return: Return True 
        """
        # TODO: Implement
        valid_cells = []
        original_cell = self.cell
        reachable_cells = self.get_reachable_cells()

        for target_cell in reachable_cells:
            captured = self.board.get_cell(target_cell)

        # Zug simulieren
            self.board.set_cell(target_cell, self)

        # Prüfen, ob eigener König im Schach steht
            if not self.board.is_king_check_cached(self.white):
                valid_cells.append(target_cell)

        # 
            self.board.set_cell(original_cell, self)
            self.board.set_cell(target_cell, captured)

        return valid_cells

class Pawn(Piece):  # Bauer
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanik for `pawns <https://de.wikipedia.org/wiki/Bauer_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Pawns can move only forward (towards the opposing army). Depening of whether this piece is black of white, this means pawn
        can move only to higher or lower rows. Normally a pawn can only move one cell forward as long as the target cell is not occupied by any other piece. 
        If the pawn is still on its starting row, it can also dash forward and move two pieces at once (as long as the path to that cell is not blocked).
        Pawns can only hit diagonally, meaning they can hit other pieces only the are one cell forward left or one cell forward right from them. 

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the pawn movability mechanics. 

        **NOTE**: For all you deep chess experts: Hitting `en passant <https://de.wikipedia.org/wiki/En_passant>`_ does not need to be implemented.
        
        :return: A list of reachable cells this pawn could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move
        row, col = self.cell
        direction = 1 if self.white else -1
        reachable_cells = []


        # Ein Feld vor
        one_step = (row + direction, col)
        if self.board.cell_is_valid_and_empty(one_step):
            reachable_cells.append(one_step)

            # Zwei Felder vor (nur Startposition)
            start_row = 1 if self.white else 6
            two_step = (row + 2 * direction, col)
            if row == start_row and self.board.cell_is_valid_and_empty(two_step):
                reachable_cells.append(two_step)

        # Diagonal schlagen
        for dcol in (-1, 1):
            target = (row + direction, col + dcol)
            if self.can_hit_on_cell(target):
                reachable_cells.append(target)

        return reachable_cells

class Rook(Piece):  # Turm
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for `rooks <https://de.wikipedia.org/wiki/Turm_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Rooks can move only horizontally or vertically. They can move an arbitrary amount of cells until blocked by an own piece
        or an opposing piece (which they could hit and then being stopped).

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this rook could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move
        cells = []
        row, col = self.cell

        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while True:
                cell = np.array([r, c])
                if self.board.cell_is_valid_and_empty(cell):
                    cells.append(cell)
                elif self.can_hit_on_cell(cell):
                    cells.append(cell)
                    break
                else:
                    break
                r += dr
                c += dc

        return cells

class Knight(Piece):  # Springer
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for `knights <https://de.wikipedia.org/wiki/Springer_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Knights can move in a special pattern. They can move two rows up or down and then one column left or right. Alternatively, they can
        move one row up or down and then two columns left or right. They are not blocked by pieces in between. 

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this knight could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move
        # Zellen die der Springer von Seiner Position errreichen kann
        cells = []                                  # Leere Liste, die alle erreichbaren Felder abspeichert
        row, col = self.cell                        # Aktuelle Zeile, Spalte der Figur

        directions = [                                   # Alle möglichen Spielzüge des Springers [L-Form]
            (2,1), (2,-1), (-2,1), (-2,-1),
            (1,2), (1,-2), (-1,2), (-1,-2)
        ]

        for dr, dc in directions:                        # dr - Änderung der Zeile / dc - Änderung der Spalte
            cell = np.array([row + dr, col + dc])   # Speichert Neue Position nach dem Sprung als Array
            if self.can_enter_cell(cell):           # Kann die Figur das Feld betreten   
                cells.append(cell)                  # Wird in die Liste Cells eingefügt

        return cells                                # Gibt alle gültigen Felder zurück auf die der Springer drauf kann  



class Bishop(Piece):  # Läufer
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for `bishop <https://de.wikipedia.org/wiki/L%C3%A4ufer_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Bishops can move diagonally an arbitrary amount of cells until blocked.

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this bishop could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move
        
        cells = []                                              # Leere Liste die alle erreichbaren Felder abspeichert
        row, col = self.cell                                    # Aktuelle Zeile und Spalte der Figur

        directions = [(1,1), (1,-1), (-1,1), (-1,-1)]           # Possible Moves (4 diagonale Richtungen)

        for dr, dc in directions:                               # Geht jede Mögliche Richtung durch (Änderung der Zeile, Spalte)
            r, c = row + dr , col + dc                          # Erstes Feld in die Richtung
            while True:                                         # Schleife wird erhöht bis Blockade erreicht ist
                cell = np.array([r, c])                         # Speichert die neue Position in einem Array ab
                if self.board.cell_is_valid_and_empty(cell):    # Leer und Valid
                    cells.append(cell)                          # Feld wird Zelle hinzugefügt
                elif self.can_hit_on_cell(cell):                # Kann Figur schlagen
                    cells.append(cell)                          # Feld wird Zelle hinzugefügt
                    break                                       # Stoppt weil der Springer nicht darüber hinausziehen kann
                else:
                    break                                       # Wenn das Feld nicht leer ist und keine gegnerische Figur drauf ist break (keine Valid Cell, Eigene Figur))
                r += dr                                         # Schritt in die gleiche Richtung (row)
                c += dc                                         # Schritt in die gleiche Richtung (col)

        return cells                              

class Queen(Piece):  # Königin
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for the `queen <https://de.wikipedia.org/wiki/Dame_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Queens can move horizontally, vertically and diagonally an arbitrary amount of cells until blocked. They combine the movability
        of rooks and bishops. 

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this queen could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move
        cells = []                                              # Erstelle eine Leere Liste für alle erreichbaren Zellen
        row, col = self.cell                                    # Aktuelle Position der Dame

        directions = [                                          # Alle möglichen Richtungen, welche die Dame gehen kann
            (1,0), (-1,0), (0,1), (0,-1),
            (1,1), (1,-1), (-1,1), (-1,-1)
        ]

        for dr, dc in directions:                               # Geht alle möglichen Richtungen durch
            r, c = row + dr, col + dc                           # Erstes Feld in die Richtung
            while True:                                         # Schleife wird erhöht bis Blockade erreicht ist (while True immer 1 Schritt weiter)
                cell = np.array([r, c])                         # Neue Position der Dame wird in einem Array gespeichert (row,col)
                if self.board.cell_is_valid_and_empty(cell):    # Wenn Zelle gültig und leer ist
                    cells.append(cell)                          # Feld wird Zelle hinzugefügt
                elif self.can_hit_on_cell(cell):                # Wenn Figur in der Zelle geschlagen werden kann
                    cells.append(cell)                          # Feld wird Zelle hinzugefügt
                    break                                       # break weil nach dem capture kein weiteres Feld weitergezogen werden kann
                else:
                    break                                       # break wenn kein valides Feld mehr frei ist (eigenes Piece, ausßerhalb des Felds)
                r += dr                                         # Schritt in die gleiche Richtung (row)
                c += dc                                         # Schritt in die gleiche Richtung (col)

        return cells                                            # Gibt alle gültigen Felder zurück auf die die Dame gehen kann

class King(Piece):  # König
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for the `king <https://de.wikipedia.org/wiki/K%C3%B6nig_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Kings can move horizontally, vertically and diagonally but only one piece at a time.

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this king could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move
        cells = []                                              # Leere Liste mit den erreichbaren Feldern
        row, col = self.cell                                    # Aktuelle Position des Königs

        directions = [                                          # Bewegungsmöglichkeiten
            (-1,-1), (-1,0), (-1,1),
            (0,-1)     ,     (0,1),
            (1,-1),  (1,0),  (1,1)
        ]

        for dr, dc in directions:                               # Geht alle möglichen Felder durch auf die der König kann
            cell = np.array([row + dr, col + dc])               # Neue Position wird in einem Array gespeichert             
            if self.board.cell_is_valid_and_empty(cell):        # Zelle ist gültig und leer
                cells.append(cell)                              # Feld wird in cell hinzugefügt
            elif self.can_hit_on_cell(cell):                    # König kann den Gegner schlagen          
                cells.append(cell)                              # Feld wird in cell hinzugefügt                      
                                                       

        return cells                                            # # Gibt alle gültigen Felder zurück auf die der König gehen kann                                  