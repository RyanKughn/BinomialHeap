"""
Implementation of a binomial heap.

@author: Ryan Kughn

Created: Q4 of 2019

Description: used to implement a binary heap with a time complexity of O(log n)

Supports The Use of:
    insert
    minimum
    extract_min
    binomial_heap_union
    decrease_key
    delete
    print_heap_helper
"""

"""
Class to create the individual nodes to be used in the binomial trees and heaps.
"""


class Node:

    # ctor
    def __init__(self, val=None, par=None, chi=None, sib=None, deg=0):
        self.parent = par
        self.key = val
        self.degree = deg
        self.child = chi
        self.sibling = sib

    # Accessor for parent
    def get_parent(self):
        return self.parent

    # Accessor for key
    def get_key(self):
        return self.key

    # Accessor for degree
    def get_degree(self):
        return self.degree

    # Accessor for child
    def get_child(self):
        return self.child

    # Accessor for sibling
    def get_sibling(self):
        return self.sibling

    # Mutator for setting parent
    def set_parent(self, par):
        self.parent = par

    # Mutator for setting key
    def set_key(self, val):
        self.key = val

    # Mutator for setting degree
    def set_degree(self, deg):
        self.degree = deg

    # Mutator for increasing the degree by 1
    def increase_degree(self):
        self.degree = self.degree + 1

    # Mutator for setting child
    def set_child(self, chi):
        self.child = chi

    # Mutator for setting sibling
    def set_sibling(self, sib):
        self.sibling = sib


"""
Class to use nodes to create the binomial trees from nodes.
"""


class BinomialTree:
    # ctor
    def __init__(self, val=None, par=None, chi=None, sib=None, deg=0):
        node = Node(val, par, chi, sib, deg)
        self.head = node
        self.degree = deg

    # Accessor for the degree of tree
    def get_degree(self):
        return self.degree

    # Accessor for the head of the tree
    def get_head(self):
        return self.head

    # Accessor for the sibling of the tree
    def get_sibling(self):
        tmp = self.head
        return tmp.get_sibling()

    # Inserts a node into an empty tree
    def insert(self, node):
        tmp = Node(node, 0)
        self.head = tmp
        self.degree = 0

    # Links two trees together
    def binomial_tree_link(self, sm_hd):
        lg_hd = self.get_head()

        lg_hd.set_parent(sm_hd)
        lg_hd.set_sibling(sm_hd.get_child())
        sm_hd.set_child(lg_hd)
        sm_hd.increase_degree()


"""
Class that creates a heap out of binomial trees.
"""


class BinomialHeap:

    def __init__(self, head=None, size=1):
        if head is None:
            self.head = None
            self.size = 0

        else:
            self.head = Node(head)
            self.size = size

    def get_head(self):
        return self.head

    # Unites any trees of the same degree together to maintain heap property
    def binomial_heap_union(self, lhs, rhs):

        # Prepare a new heap to be filled with the meld of lhs and rhs
        heap = BinomialHeap()
        heap.binomial_heap_merge(lhs, rhs)
        curr = heap.head
        nxt = heap.head.get_sibling()
        prev = Node(None)

        # This will fill in the new heap
        while nxt is not None:
            # Cases one and two
            # print("while loop")
            # heap.print_heap_helper()
            nxt_sib = nxt.get_sibling()
            if (curr.get_degree() is not nxt.get_degree() or
                    nxt_sib is not None and nxt_sib.get_degree() is curr.get_degree()):
                prev = curr
                curr = nxt

            # Case three
            elif curr.get_key() <= nxt.get_key():
                curr.set_sibling(nxt.get_sibling())
                BinomialTree(nxt.get_key(), nxt.get_parent(), nxt.get_child(),
                             nxt.get_sibling(), nxt.get_degree()).binomial_tree_link(curr)
                heap.size = heap.size - 1

            # Case four
            else:
                if prev.get_key() is None:
                    heap.head = nxt

                else:
                    prev.set_sibling(nxt)

                BinomialTree(curr.get_key(), curr.get_parent(), curr.get_child(),
                             curr.get_sibling(), curr.get_degree()).binomial_tree_link(nxt)
                curr = nxt
                heap.size = heap.size - 1

            nxt = curr.get_sibling()

        # Here is where the self parameters are changed to account for the new heap created
        self.head = heap.head
        self.size = heap.size

    # Merges two heaps together
    def binomial_heap_merge(self, lhs, rhs):

        # Set up pointers to be used to iterate the heaps
        self.size = lhs.size + rhs.size
        lhs_ptr = lhs.head
        rhs_ptr = rhs.head
        slf_ptr = self.head

        # Iterate through the heaps merging them together, basically merge two sorted lists into one
        while lhs_ptr is not None or rhs_ptr is not None:

            # if and elif are for when either heap runs out of trees
            if lhs_ptr is None:

                # For the case of one of the heaps being None from the start
                if slf_ptr is None:
                    self.head = rhs_ptr
                    rhs_ptr = None

                else:
                    slf_ptr.set_sibling(rhs_ptr)
                    rhs_ptr = None

            elif rhs_ptr is None:

                # For the case of one of the heaps being None from the start
                if slf_ptr is None:
                    self.head = lhs_ptr
                    lhs_ptr = None

                else:
                    slf_ptr.set_sibling(lhs_ptr)
                    lhs_ptr = None

            # Done to keep the new heap in increasing order of degree
            else:

                tmp1 = rhs_ptr.get_degree()
                tmp2 = lhs_ptr.get_degree()
                if rhs_ptr.get_degree() < lhs_ptr.get_degree():

                    # If the new head has not been set yet
                    if self.head is None:
                        self.head = rhs_ptr
                        slf_ptr = self.head

                    else:
                        slf_ptr.set_sibling(rhs_ptr)
                        slf_ptr = slf_ptr.get_sibling()

                    rhs_ptr = rhs_ptr.get_sibling()

                else:

                    # If the new head has not been set yet
                    if self.head is None:
                        self.head = lhs_ptr
                        slf_ptr = self.head

                    else:
                        slf_ptr.set_sibling(lhs_ptr)
                        slf_ptr = slf_ptr.get_sibling()

                    lhs_ptr = lhs_ptr.get_sibling()

    # Add a node to a heap
    def insert(self, val):

        # Simply meld a heap with the new node with the current heap
        tmp = BinomialHeap(val, 1)
        ret = BinomialHeap()
        ret.binomial_heap_union(self, tmp)

        self.head = ret.head
        self.size = ret.size
        # print("head key 1",self.head.get_key())

    # Returns the minimum key in heap
    def minimum(self):
        tmp = self.min_loop()

        return tmp.get_key()

    def make_heap(self, node):
        self.head = node

    # Returns the smallest node, and removes the node.
    def extract_min(self):

        # Get the minimum node, and store the key
        min_node = self.min_loop()
        min_key = min_node.get_key()

        # Create a heap to store the children of the min node
        if min_node.get_degree is not 0:
            heap = BinomialHeap()
            min_node.get_child().set_parent(None)
            heap.make_heap(min_node.get_child())
            heap.size = min_node.get_degree()

            curr = heap.head
            nxt = curr.get_sibling()

            # Sort the children in descending order of degree
            while True:

                if nxt is None:
                    break

                nxt.set_parent(None)

                tmp = nxt.get_sibling()
                nxt.set_sibling(heap.head)
                curr.set_sibling(tmp)

                heap.head = nxt

                nxt = curr.get_sibling()

        # Removes the old tree from the list
        hd = self.head
        prv = None
        nt = hd.get_sibling()
        while hd is not None:

            if hd is min_node:

                if prv is None:
                    self.head = nt

                else:
                    prv.set_sibling(nt)

                break

            else:
                prv = hd
                hd = nt
                nt = hd.get_sibling()

        # Only union if min node has children
        if min_node.get_degree() is not 0:
            new = BinomialHeap()
            new.binomial_heap_union(self, heap)

            self.head = new.head
            self.size = new.size

        return min_key

    # Helper method for my min methods
    def min_loop(self):
        it = self.head
        min_key = float('inf')
        min_node = None

        # Loop to find the min and store the key and node
        while it is not None:

            if it.get_key() < min_key:
                min_key = it.get_key()
                min_node = it

            it = it.get_sibling()

        return min_node

    # Used to decrease the value of a key and percolate up if need be
    def decrease_key(self, node, val):
        node.set_key(val)

        # Moves up to the parent of the containing tree
        while node.get_parent() is not None:
            tmp = node.get_parent()

            if tmp.get_key() <= node.get_key():
                break

            tmp_key = tmp.get_key()
            tmp.set_key(node.get_key())
            node.set_key(tmp_key)

        return self

    # Used to start off the recursive print method
    def print_heap_helper(self):
        tab = 0
        self.print_heap(self.head, tab)
        print('\n')

    # Recursive method to print out a heap
    def print_heap(self, node, tab):
        spc = " "
        spc = spc * tab
        print(spc, node.get_key())

        # Print all children with an increased tab
        if node.get_child() is not None:
            self.print_heap(node.get_child(), tab + 1)

        # Print all siblings at the same tab
        if node.get_sibling() is not None:
            self.print_heap(node.get_sibling(), tab)

    # Used to delete any node
    def delete(self, node):
        # Make the node a new minimum of the heap
        self.decrease_key(node, float("-inf"))

        # Extract said new min
        self.extract_min()


def main():
    bin1 = BinomialHeap(34)

    bin2 = BinomialHeap(21)

    bin3 = BinomialHeap()

    bin3.binomial_heap_union(bin1, bin2)

    print("bin3 print")
    bin3.print_heap_helper()

    # bin3.extract_min()

    head = bin3.get_head()

    chi = head.get_child()

    bin3.decrease_key(chi, 15)

    bin3.insert(12)
    print("bin3 ins")
    bin3.print_heap_helper()

    head = bin3.get_head()
    sib = head.get_sibling()
    chi = sib.get_child()

    bin3.delete(chi)

    print("bin3 del")
    bin3.print_heap_helper()


if __name__ == '__main__':
    main()
