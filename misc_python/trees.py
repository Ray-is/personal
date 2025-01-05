class Node:
    def __init__(self, val, l=False, r=False):
        self.val = val
        self.l = l
        self.r = r

    def get_height(self):
        lh = 1 + self.l.get_height() if self.l else 1
        rh = 1 + self.r.get_height() if self.r else 1
        return lh if lh >= rh else rh

    def count(self):
        stack = []
        count = 0
        curr = self
        while stack or curr:
            if curr:
                stack.append(curr)
                curr = curr.l
            else:
                curr = stack.pop().r; count += 1
        return count


    def print_level(self, lvl):
        if lvl == 0:
            print(self.val, end=' ')
        if self.l:
            self.l.print_level(lvl - 1)
        if self.r:
            self.r.print_level(lvl - 1)

    def print_levels(self):
        for i in range(self.get_height()):
            self.print_level(i)
            print()

    def print_inorder(self):
        if self.l:
            self.l.print_inorder()
        print(self.val, end=' ')
        if self.r:
            self.r.print_inorder()

    def print_preorder(self):
        print(self.val, end=' ')
        if self.l:
            self.l.print_preorder()
        if self.r:
            self.r.print_preorder()

    def print_postorder(self):
        if self.l:
            self.l.print_postorder()
        if self.r:
            self.r.print_postorder()
        print(self.val, end=' ')

    def print_postorder1(self):
        stack = []
        curr = self
        while True:
            if curr.r:
                stack.append(curr.r)
            stack.append(curr)
            curr = curr.l

    def mitosis(self, n=1):
        if n == 0:
            return
        self.l, self.r = Node(self.val), Node(self.val)
        self.l.mitosis(n - 1)
        self.r.mitosis(n - 1)

    def invert(self):
        self.l, self.r = self.r, self.l
        if self.l:
            self.l.invert()
        if self.r:
            self.r.invert()

tree = Node(0)
tree.l = Node(1)
tree.r = Node(2)
tree.print_postorder1()