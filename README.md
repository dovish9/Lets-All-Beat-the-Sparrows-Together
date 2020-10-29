# **다같이 참새를 때려잡자** 〈Let's All Beat the Sparrows Together〉

## **version: 1.0.7**
made with `pygame`, made by `whitedove428`

## Quick Setup

### 파이썬 설치

[여기](https://www.python.org/downloads/)에서 파이썬을 설치. 3.8까지 정상 작동했고 3.9 이상에서 될지 모르겠음.

### 패키지 설치

```
pip install pygame
pip install numpy
```

처음 파이썬을 깔았다면 같이 깔리는 pip(패키지 관리 도구)이 구버전이라 오류 메시지가 출력될 수 있음.
차분히 메시지대로

```
pip install --upgrade pip
```
을 통해 최신 버전으로 업그레이드.

## 사용 전 주의사항

### 게임 실행

윈도우라면 명령 프롬프트, 리눅스나 Mac 등은 터미널을 실행한다.

```
cd [경로]
```
를 입력한다.

게임을 실행하고 싶다면

```
python game.pyw
```

를 입력한다.

(확장자가 pyw면 파이썬 쉘이나 터미널 없이 실행된다.)

### 점수판 초기화

```
python initiate_scoreboard.py
```

점수판은 게임이 오버되면 표시되고 직접 옵션에서 볼 수도 있다.

## 해로운 새를 때려죽이자
* 플레이타임: 10분 내외

* 메뉴에서 60 프레임, 게임 스테이지에서 24프레임

* 메뉴에서는 주로 방향키와 엔터 키로 조작

* F11: 전체화면

* ESC: 옵션 (게임 스테이지에서만)

* initiate_scoreboard로 점수판을 초기화할 경우 복구할 수 없음

* 인게임 조작법: Menu → Option → Controls에 대략 첨부

![guideline](./screenshots/controls_guideline.png)

# 게임 플레이

## 새총
* 허공에 체공할 수 있는 돌은 최대 `6`개(렉을 줄이기 위해 제한)
* `Shoot!`: 발사 가능
* `Wait!`: 돌이 바닥에 떨어질 때까지 대기
* 최대 대미지는 120가량

## 패배 조건
1. `생명력`이 0이 됐을 때
2. `밀밭 내구도`가 0이 됐을 때

## 음식 목록
| 음식 | 비고 |
|:---:|:---:|
| 포션 | 1.5hearts 회복 |
| 포션(뚱캔) | 3.0hearts 회복 |
| 관통 캔 | 스파이어 철거 시 드랍 |
| 샷건 캔 | 인면조 처치 시 드랍 |
| 빠른 장전 캔 | 추가 목표 달성 시 드랍 |

## 해로운 새 목록
| 해로운 새 | 유형 | 체력 | 비고 |
|:---:|:---:|---:|:---:|
| 참새 | 일반 | 1 |  |
| 타조 | 일반 | 1 |  |
| 정예타조 | 정예 | 200 |  |
| 뮤탈리스크 | 정예 | 300 |  |
| UFO | 일반 | 1 |  |
| 인면조 | 우두머리 | 2880 |  |
| 무리군주 | 정예 | 1500 | 공생충을 소환 |
| 공생충 | 일반 | 1 |  |
| 메디브 | 우두머리 | 5760 |
| 비둘기 | 번외 | 1 |  |
| 까마귀 | 번외 | 1 |  |
| 두루미 | 번외 | 1 |  |
| 펠리컨 | 번외 | 1 |  |
| 앵무새 | 번외 | 1 |  |

## 구조물 목록
| 구조물 | 체력 | 비고 |
|:---:|---:|:---:|
| 스파이어 | 6000 | 뮤탈리스크를 소환 |
| 그레이터 스파이어 | 12000 | 뮤탈리스크, 무리군주를 소환 |

## 투사체 목록
| 투사체 | 대미지 | 비고 |
|:---:|---:|:---:|
| 돌 | 0~120 | 플레이어가 발사 |
| 쐐기벌레 | 0.5hearts | 뮤탈리스크가 발사 |
| 레이저빔 | 1.0hearts | UFO가 발사 |
| 새똥 | 1.0hearts | 참새가 배변 |
| 비전균열 | 1.0hearts | 메디브가 발사 |

## 아직 수정되지 않은 버그

\-

# 스크린샷

## 게임플레이 영상
[유튜브에서 보기](https://www.youtube.com/watch?v=CkQKDU5AZGs&feature=youtu.be)

## Title
![image0](./screenshots/unknown0.png)

## Menu
![image1](./screenshots/unknown1.png)

![image2](./screenshots/unknown2.png)

![image3](./screenshots/unknown3.png)

## befor Game
![image4](./screenshots/unknown4.png)

![image5](./screenshots/unknown5.png)

## in Game
![image6](./screenshots/unknown6.png)

![image7](./screenshots/unknown7.png)

![image8](./screenshots/unknown8.png)

![image9](./screenshots/unknown9.png)

![image10](./screenshots/unknown10.png)

![image11](./screenshots/unknown11.png)

![image12](./screenshots/unknown12.png)

## after Game
![image13](./screenshots/unknown13.png)

![image14](./screenshots/unknown14.png)

## Statistics & Board
![image15](./screenshots/unknown15.png)

![image16](./screenshots/unknown16.png)

# 여담

## 문제점

1. 첫째로 미숙한 상태에서 만든 스파게티 코드. 돌과 충돌하면 삭제되는 일반 새를 만들고 생명력이 있는 정예 새를 만들었는데, 일반 새도 애초에 생명력이 1인 정예 새로 만들었으면 상당히 코드가 간결해졌을 것이다. 

1. C/C++에서는 잘만 되던 Backspace '\b'가 안 먹힌다. 이것 때문에 점수판 만드는 데 상당히 고생했다.

1. 플레이어는 클래스를 배우기 전에 만들어서 객체가 아니다. 객체로 만들었으면 2player도 쉽게 만들 수 있을 텐데 좀 아쉽다. 그래도 객체가 아니었던 돌을 객체로 뜯어고치면서 고생을 실컷 했기 때문에 이제 와서 바꿀 생각이 없다. ㅎ.ㅎ

1. 본 게임 안에서만 24프레임이다. 이게 말할 것이 많은 게, 'pygame.image.load()'를 할 때마다 뒤에 .convert()나 convert_alpha()를 붙이지 않으면 매 틱마다 이미지를 로드한다고 한다. 스텍오버플로우에서 그렇게 말했다. 실제로 제보니 60프레임으로 설정해놓은 것이 24프레임으로 나왔다. 그래서 전부 수정한다음 게임 스테이지에서만 24프레임으로 바꿨다. (convert()와 convert_alpha()의 차이는 후자가 투명색을 지원한다는 것.) 참새 같은 경우는 속력이 3~4 정도 되는데 이걸 60프레임으로 했으면 정수만 지원하는 pygame에서 어떻게 만들었을까 하는 생각도 든다. 잘된 일인가…….

1. 그 많은 텍스트들을 만들 때 배경을 투명하게 할 경우 하나당 7줄 정도를 차지한다. 처음부터 함수를 만들어서 텍스트를 생성할 걸 하는 생각이 든다.

1. 많은 사진을 다른 곳에서 따왔다. 메탈슬러그에서 관통, 샷건, 퀵차지의 아이콘과 UFO를, 스타크래프트에서 스파이어, 그레이터 스파이어, 뮤탈리스크, 무리군주를, 히어로즈 오브 더 스톰에서 포션과 메디브를, 평창 동계 올림픽에 등장하여 특유의 기괴함으로 유명했던 인면조를 사용했다.

1. 보스 인면조에서 패턴을 만든다고 "춤을 추지 않으면 잡아먹을 테야!"라는 대사를 달아놓고 플레이어가 왼쪽 오른쪽으로 움직이지 않으면 참새가 똥을 싸게 만들었다. 결과물은 심히 조잡하기가 이를 데가 없다.

1. 최종 보스 메디브의 생김새를 자세히 보면 구멍이 숭숭 뚫려있다. 전부 다른 게임에서 캡처해 포토샵으로 지운 것이기 때문이다. 구멍 뚫린 부분은 원래 체력바와 닉네임이 있던 자리다.

1. 포토샵이 png 파일에 표준이 아닌 데이터를 써놓는다고 한다. 실행이 안 되진 않지만 거슬리게 오류 메시지를 띄웠었는데, 구글링으로 없애는 방법을 알아냈다. [ImageMagick](https://imagemagick.org/index.php)을 깐다. 윈도우에서 설치를 하는 경우 'Install legacy utilities (e.g. convert)'를 체크한다. 이걸 해야지 명령 프롬프트에서 일괄 변환을 할 수 있다. 그리고 배치 파일을 만든다. 실행하면 같은 폴더에 있는 모든 png 파일이 변환된다.

```python
# pygame 텍스트 투명 배경 설정
text = arcadeFont35.render('대충 텍스트', True, (255, 255, 255))
textRect = text.get_rect()
textRect.centerx = windowSurface.get_rect().centerx
textRect.centery = windowSurface.get_rect().centery+320
alpha_img = pygame.Surface(text.get_size(), pygame.SRCALPHA)
alpha_img.fill((255, 255, 255, 255))
text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
```

```batch
:: ImageMagick의 convert [입력] -strip [출력]
@echo off
echo All files in format png will be converted.
for %%i in (*.png) do (
convert %%i -strip %%i
echo %%i converted
)
pause
```
## 뮤탈리스크의 이동 경로

매개변수 θ를 사용하여 나타낼 수 있다.

![equation1](./screenshots/equation1.png)

![result1](./screenshots/result1.png)
![result2](./screenshots/result2.png)
![result3](./screenshots/result3.png)

그래프의 모양을 가다듬기 위해서 아래 식을 곱한다.(scaling)

![equation2](./screenshots/equation2.png)

아래와 같이 표현된다.

![equation3](./screenshots/equation3.png)

![graph](./screenshots/graph.png)

θ 값에 따른 점

![gif](./screenshots/graph.gif)

이를 활용하여 뮤탈리스크의 이동 경로를 만들 수 있다.