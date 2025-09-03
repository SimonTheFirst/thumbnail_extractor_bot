import pytest

from thumbnail_extractors import thumbnail_extractor_factory


def test_get_vk_extractor():
    extractor = thumbnail_extractor_factory('vk')
    assert extractor.__name__ == 'extract_vk_thumbnail'

def test_get_vkvideo_extractor():
    extractor = thumbnail_extractor_factory('vkvideo')
    assert extractor.__name__ == 'extract_vk_thumbnail'

def test_get_rutube_extractor():
    extractor = thumbnail_extractor_factory('rutube')
    assert extractor.__name__ == 'extract_rutube_thumbnail'

def test_get_youtube_extractor():
    extractor = thumbnail_extractor_factory('youtube')
    assert extractor.__name__ == 'extract_youtube_thumbnail'

def test_get_youtu_be_extractor():
    extractor = thumbnail_extractor_factory('youtu')
    assert extractor.__name__ == 'extract_youtube_thumbnail'

def test_invalid_extractor():
    with pytest.raises(ValueError):
        thumbnail_extractor_factory('liveleaks')
