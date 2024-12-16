import requests


class SplayTreeNode:
    def __init__(self, key, value):
        self.key = key  # URL
        self.value = value  # HTML
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    def _zig(self, node):
        # Правый
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        return left_child

    def _zag(self, node):
        # Левый
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        return right_child

    def _splay(self, node, key):
        # Поднятие узла к корню
        if not node or node.key == key:
            return node

        if key < node.key:
            if not node.left:
                return node
            if key < node.left.key:
                node.left.left = self._splay(node.left.left, key)
                node = self._zig(node)
            elif key > node.left.key:
                node.left.right = self._splay(node.left.right, key)
                if node.left.right:
                    node.left = self._zag(node.left)
            return self._zig(node) if node.left else node

        else:
            if not node.right:
                return node
            if key > node.right.key:
                node.right.right = self._splay(node.right.right, key)
                node = self._zag(node)
            elif key < node.right.key:
                node.right.left = self._splay(node.right.left, key)
                if node.right.left:
                    node.right = self._zig(node.right)
            return self._zag(node) if node.right else node

    def insert(self, key, value):
        if not self.root:
            self.root = SplayTreeNode(key, value)
            return
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            self.root.value = value
            return
        new_node = SplayTreeNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

    def find(self, key):
        if not self.root:
            return None
        self.root = self._splay(self.root, key)
        return self.root.value if self.root.key == key else None


class PageCache:
    def __init__(self):
        self.cache = SplayTree()

    def get_page(self, url):
        cached_page = self.cache.find(url)
        if cached_page:
            print("Страница взята из кэша.")
            return cached_page
        print("Страница запрошена из интернета.")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.text
                self.cache.insert(url, html_content)
                return html_content
            else:
                print("Ошибка: страница не найдена.")
                return None
        except Exception as e:
            print(f"Ошибка при запросе страницы: {e}")
            return None


if __name__ == "__main__":
    page_cache = PageCache()
    url = "https://yandex.ru"

    # загрузка
    print(page_cache.get_page(url))

    # из кэша
    print(page_cache.get_page(url))
