import pytest

from thumbnail_extractors.vk.exctractor import _get_video_id_from_url


@pytest.mark.parametrize('url, expected_id', [
    ('https://vkvideo.ru/video-215474125_456240842', '-215474125_456240842'),
    ('https://vkvideo.ru/video79833549_456239994', '79833549_456239994'),
    ('https://vk.com/mir24tv?from=groups&z=video-23712441_456299797%2Fvideos-23712441%2Fpl_-23712441_-2', '-23712441_456299797'),
    ('https://vk.com/havoc_b?z=video-224770153_456239067%2Fvideos1492599%2Fpl_1492599_-2', '-224770153_456239067')
])
def test_get_id_from_url(url, expected_id):
    assert _get_video_id_from_url(url) == expected_id
