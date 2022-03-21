from difflib import SequenceMatcher

class Filter():
    def __init__(self, threshold, **kwargs):
        self.threshold = threshold
        self.kwargs = kwargs
    
    def __call__(self, message):
        raise NotImplementedError('__call__ not implemented')

class FilterPipeline():
    def __init__(self, filters):
        self.filters = filters
    
    def __call__(self, message):
        for filter in self.filters:
            if filter(message):
                return True
        return False

class KeywordFilter(Filter):
    def __init__(self, threshold=None, **kwargs):
        super().__init__(threshold, **kwargs)

    def __call__(self, message):
        for banned_word in self.kwargs['syntax_filter_words']:
            if banned_word in message.lower():
                return True
        return False

class SyntaxFilter(Filter):
    def __init__(self, threshold=0.8, **kwargs):
        super().__init__(threshold, **kwargs)
        if 'syntax_filter_threshold' in self.kwargs:
            self.threshold = self.kwargs['syntax_filter_threshold']
    
    def __call__(self, message):
        for banned_word in self.kwargs['syntax_filter_words']:
            for word in message.split(' '):
                if SequenceMatcher(None, banned_word, word).ratio() > self.threshold:
                    return True
        return False

class SemanticFilter(Filter):
    def __init__(self, threshold=0.8, **kwargs):
        super().__init__(threshold, **kwargs)
        if 'semantic_filter_threshold' in self.kwargs:
            self.threshold = self.kwargs['semantic_filter_threshold']
    
    def __call__(self, message):
        raise NotImplementedError('__call__ not implemented -- yet.')
