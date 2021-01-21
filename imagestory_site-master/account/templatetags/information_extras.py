# templates 태그 새로 만들어서 적용하기
from django import template
from account.models import Commentalert, Profile
from category.models import Category
register = template.Library()

# Board 좋아요 용 확인
@register.filter
def alert_checking(obj , user):
    try:
        getProfile = Profile.objects.get(nickname=user) #안됬는데 보니깐 슈퍼유저는 Profile이 안만들어져서 찾지를 못하는 것이였음
        comment_a = Commentalert.objects.get(profile=getProfile)
        if getProfile.alert == comment_a.recent:
            return '<svg version="1.1" class = "svg-icon" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="46px" height="51px" viewBox="0 0 46 51" enable-background="new 0 0 46 51" xml:space="preserve">  <image id="image0" width="46" height="51" x="0" y="0" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAzCAQAAABC+PL5AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QA/4ePzL8AAAAJcEhZcwAACxIAAAsSAdLdfvwAAAAHdElNRQflARULJAlUmxhvAAACeElEQVRYw+2YsW8TMRSHP5eCFKQmUTqwBPUYsjaRGJI3JZmQMh3qWsSxMOc/aJhgbBlZmgpGkCKGSExcWdwOSLRrBlIpS4eitAOREJIZLi0lveZ813RB/W337Pfppyfbz2dlsJO4tMlwjKt9yxSUNXxIBoBjnbWFz9lOHKMhI45tyryVaweXX9wB4Ddt8enobzMoi9RoUQ0ZOKDNuh4mhotDOwAvUyA/jh7RY58RoE7MU91JBBdPbZh0ijplFi+M7tDlB8CW9mLDxWMTCqyGgE/VpQuwjRtenkvgAbrME6Zrn7eMLnUfCpeS+mIWotEAA14BvNCti2Ph67xtFgpWaMizCrAmJSu4eBRTPLdCA1RYBli3c96CBilrOKwAVKUWCReXpRT1GGhYpAzgRTt3CabGUh1Qj6PhNajEhufJYdKThZmAi8MSZxs9jgpjY9OcO+NpsbU4zp4GzyYinzqPgJeSOg+TfSe6gd/Ab+D/M1wcmleiVcULgYsjbRnynUzSg6tADmBTjHTEDWLKAOKp12YBIEcjQR8KNOADvdOPLe2BMkiNz1BgJVEHmtQRu8Elb0M3lUF8qssx7inR2uEdwINbn0q8TNHk9gzheQYcwvFc0HviXIFsVAGozeEk6/bTFZi9/k3085rg8/TBB+7OFLsHMFSVLD7FazFeVwbJ4k5eZ86pwqN7PJwIHvI1+Fm8TEM6uh/9H9pirUFjItpjA7Z1bXpu9Grp8/fEONORVV2i4T70LsB2ATpXhus+2/CG0bnYe3qokykVH8viSUQctWfSORoUSTGgyz7AMz0LOEhJfTT3/wlZoK0fcyRLE5cicIBPS/dtsv4AlrujPRXZlcYAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMDEtMjFUMTE6MzY6MDkrMDA6MDD3/+haAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTAxLTIxVDExOjM2OjA5KzAwOjAwhqJQ5gAAAABJRU5ErkJggg==" /></svg>'
        else:
            return '<svg version="1.1" class = "svg-icon" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="46px" height="51px" viewBox="0 0 46 51" enable-background="new 0 0 46 51" xml:space="preserve">  <image id="image0" width="46" height="51" x="0" y="0" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAzCAMAAADfL8pAAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAflBMVEX///9gOBtgOBtgOBtgOBtgOBtgOBtgOBtgOBtgOBtgOBtgOBtgOBthOBthORtgOBtgOBtgOBtgOBtgOBtpPxphORtgOBtpPxmbZRG5ewzXkgeRXRPDgwr1qAL/sACvdA59ThZzRxjNigiHVhTroQPhmQWlbA+HVhWCUhX///9O2N/MAAAAFnRSTlMAEMCgcGCAMNjO4NBA8eIgUJDwsP7yw87lmwAAAAFiS0dEAIgFHUgAAAAJcEhZcwAACxIAAAsSAdLdfvwAAAAHdElNRQflARULHRw3wnE+AAABVklEQVRIx+2W2ZpDQBCFxdJmgixm5iAoS5aZ93/Cqc72SVTTuc9/60f1wWmOI7BwAc+xxgcTWOuu1pWlHKoPrX/6oYUcLHEnmhsoZjnLix1TlPqEyTsolquartRNNrliD8jv8vmEciJRtit6ogB8wyIFm6gCYsleJGhIIMdqIY7SSjbVnfTE1sBO1KlHMr68wp4MdEKaS/QmvYIrzGKy6QA86xvzLETtKEslp3ihHA0/qTejKN/6W3e2L+kxzF+Hbo900GbxV8rtVZv1A7dZ6oW3OZj2SBP03b3xufvzA81y5P7bnNuomJc13E+66lo7WxfIZjrBR06cp2sqLzn+l/X+Fd1D1ljyzXqYwpp0ze3oqyERfm9X+4P7cCgQtoXBWhqLnXvwHHILPUB3fTfrDBbb/Ar5RS8Rzdvc9Njz+H2LH5t/CCdILrElsY3N0W75RyJS0m76D3Dql/k7zihUAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIxLTAxLTIxVDExOjI5OjI4KzAwOjAwIyhg3gAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMS0wMS0yMVQxMToyOToyOCswMDowMFJ12GIAAAAASUVORK5CYII=" /></svg>'
            
    except:
        Commentalert.objects.create(profile=getProfile, recent=0)
        return '<svg version="1.1" class = "svg-icon" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="46px" height="51px" viewBox="0 0 46 51" enable-background="new 0 0 46 51" xml:space="preserve">  <image id="image0" width="46" height="51" x="0" y="0" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAzCAQAAABC+PL5AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QA/4ePzL8AAAAJcEhZcwAACxIAAAsSAdLdfvwAAAAHdElNRQflARULJAlUmxhvAAACeElEQVRYw+2YsW8TMRSHP5eCFKQmUTqwBPUYsjaRGJI3JZmQMh3qWsSxMOc/aJhgbBlZmgpGkCKGSExcWdwOSLRrBlIpS4eitAOREJIZLi0lveZ813RB/W337Pfppyfbz2dlsJO4tMlwjKt9yxSUNXxIBoBjnbWFz9lOHKMhI45tyryVaweXX9wB4Ddt8enobzMoi9RoUQ0ZOKDNuh4mhotDOwAvUyA/jh7RY58RoE7MU91JBBdPbZh0ijplFi+M7tDlB8CW9mLDxWMTCqyGgE/VpQuwjRtenkvgAbrME6Zrn7eMLnUfCpeS+mIWotEAA14BvNCti2Ph67xtFgpWaMizCrAmJSu4eBRTPLdCA1RYBli3c96CBilrOKwAVKUWCReXpRT1GGhYpAzgRTt3CabGUh1Qj6PhNajEhufJYdKThZmAi8MSZxs9jgpjY9OcO+NpsbU4zp4GzyYinzqPgJeSOg+TfSe6gd/Ab+D/M1wcmleiVcULgYsjbRnynUzSg6tADmBTjHTEDWLKAOKp12YBIEcjQR8KNOADvdOPLe2BMkiNz1BgJVEHmtQRu8Elb0M3lUF8qssx7inR2uEdwINbn0q8TNHk9gzheQYcwvFc0HviXIFsVAGozeEk6/bTFZi9/k3085rg8/TBB+7OFLsHMFSVLD7FazFeVwbJ4k5eZ86pwqN7PJwIHvI1+Fm8TEM6uh/9H9pirUFjItpjA7Z1bXpu9Grp8/fEONORVV2i4T70LsB2ATpXhus+2/CG0bnYe3qokykVH8viSUQctWfSORoUSTGgyz7AMz0LOEhJfTT3/wlZoK0fcyRLE5cicIBPS/dtsv4AlrujPRXZlcYAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMDEtMjFUMTE6MzY6MDkrMDA6MDD3/+haAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTAxLTIxVDExOjM2OjA5KzAwOjAwhqJQ5gAAAABJRU5ErkJggg==" /></svg>'

@register.filter
def category_get(obj):
    all_category = Category.objects.all()
    return all_category