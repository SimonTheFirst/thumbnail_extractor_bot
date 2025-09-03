import pytest

from handlers import get_domain_name_from_url


@pytest.mark.parametrize(
    'url, expected_domain_name',
    [
        ('https://www.youtube.com/watch?v=9Ub7ipWdPO8', 'youtube'),
        ('https://youtu.be/9Ub7ipWdPO8?si=tUfdjngBfMtM85aU', 'youtu'),
        ('https://vk.com/thebatya?z=video-36965584_456249912%2Fvideos-36965584%2Fpl_-36965584_-2', 'vk'),
        ('https://rutube.ru/video/4cecfc0401b5cb5aab8d6495b918f2d9/', 'rutube'),
        ('http://rutube.ru/video/4cecfc0401b5cb5aab8d6495b918f2d9/', 'rutube'),
        ('www.rutube.kz/test_url?this=1&that=2', 'rutube'),
        ('rutube.tv/46a5s4da8s7e4asd', 'rutube'),
        ('ftp://test.com/test', 'ftp://test')
    ]
)
def test_correct_domain_names(url, expected_domain_name):
    assert expected_domain_name == get_domain_name_from_url(url)

def test_invalid_url():
    with pytest.raises(ValueError):
        url = 'thisisateststring'
        get_domain_name_from_url(url)