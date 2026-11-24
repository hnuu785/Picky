# Picky Git 협업 가이드

## 1. 저장소 받기

Git을 설치한 뒤, 프로젝트를 저장할 폴더에서 터미널을 열고 실행합니다.

```sh
git clone https://github.com/hnuu785/Picky.git
cd Picky
```

`git clone`을 하면 GitHub에서 설정한 기본 브랜치가 열립니다. `Picky` 폴더에서 다음 명령을 실행하면 작업을 시작할 `develop` 브랜치로 이동할 수 있습니다.

```sh
git switch develop
```

`develop`으로 이동한 뒤, 해당 브랜치에 기록된 버전의 LeRobot을 받습니다.

```sh
git submodule update --init --recursive
```

`origin`은 clone할 때 등록되는 GitHub 원격 저장소의 이름입니다.

## 2. 작업 브랜치 만들기

작업 브랜치는 최신 `develop`에서 만듭니다. 다른 브랜치에 있다면 먼저 `develop`으로 돌아온 뒤 아래 명령으로 원격의 최신 변경을 받습니다.

```sh
git switch develop
git pull
```

`pull`이 성공하면 `feat/작업-내용` 형식으로 브랜치를 만듭니다. 아래에서는 상품 검색 작업을 예로 듭니다.

```sh
git switch -c feat/product-search
```

이 브랜치에서 작업하고 변경 사항을 커밋합니다. `git status`로 변경한 파일과 현재 브랜치를 확인할 수 있습니다.

## 3. 검증한 작업을 develop에 합치기

1. 작업 브랜치에서 변경한 기능을 직접 실행해 보고, 관련 빌드나 테스트가 통과하는지 확인합니다.
2. 합치기 직전에 로컬 `develop`으로 이동해 **반드시 `git pull`을 먼저** 실행합니다. 문제가 생겼다면 push하지 않고 조현우 팀장에게 연락합니다.

   ```sh
   git switch develop
   git pull
   ```

3. `pull`이 성공하면 현재 브랜치인 `develop`에 작업 브랜치를 합칩니다.

   ```sh
   git merge feat/product-search --no-ff
   ```

   `--no-ff`는 병합 커밋을 만들어 작업 브랜치를 `develop`에 합친 시점을 Git 기록에 남깁니다.

4. **합쳐진 `develop`에서 같은 검사를 다시 실행합니다.** 다른 팀원의 변경과 함께 동작하는지 확인하고, 검사에 통과하면 `git push`로 로컬 커밋을 GitHub의 `develop`에 올립니다.

   ```sh
   git push
   ```

## 4. develop을 main에 반영하기

검증을 마친 `develop`의 변경을 `main`으로 반영하는 작업은 **팀장 조현우(hnuu785)만** 진행합니다.

## 5. 충돌이 났을 때

### Rebase 방식 (권장)

`develop`에 작업을 합치다가 충돌이 났다면 `git status`로 상태를 확인합니다. 병합 중이면 `git merge --abort`로 취소한 뒤 `git switch feat/product-search`처럼 본인의 작업 브랜치로 돌아갑니다.

**`feat/작업-내용` 브랜치**에서 변경을 커밋한 뒤 아래 명령을 실행합니다. 이 명령은 원격 `develop`의 최신 변경을 가져오고, 그 위에 작업 브랜치의 커밋을 다시 적용해 작업 기록을 한 줄로 이어 줍니다. [Git pull 문서](https://git-scm.com/docs/git-pull)

```sh
git pull --rebase origin develop
```

1. Rebase가 충돌로 멈추면 `git status`로 충돌 파일을 찾습니다.
2. 파일에서 `<<<<<<<`, `=======`, `>>>>>>>`로 표시된 양쪽 변경을 확인합니다. 최종 내용을 직접 정리한 뒤 충돌 표시를 지웁니다.
3. 해결한 파일마다 `git add 경로/파일명`을 실행해 해결됐다고 표시한 뒤 `git rebase --continue`를 실행합니다. 편집기가 열리면 커밋 메시지를 확인하고 저장한 뒤 닫습니다. 다음 커밋에서 충돌이 또 나면 같은 순서로 해결합니다.
4. Rebase가 끝나면 작업 브랜치에서 다시 검사한 뒤 [develop에 합치는 순서](#3-검증한-작업을-develop에-합치기)를 밟습니다.

이미 원격에 올린 작업 브랜치를 rebase하면 커밋 기록이 달라집니다. 이 경우 또는 `push`가 거절된 경우에는 작업 브랜치를 강제로 올리기 전에 조현우 팀장에게 연락합니다. **충돌이 해결되고 검사를 통과한 커밋만 `origin`에 올립니다.**

### Rebase로 해결하지 못했을 때 로컬 브랜치 복원하기

`git pull --rebase origin develop`로도 충돌을 해결하지 못했다면 **push를 중단합니다.** 현재 브랜치와 같은 이름의 브랜치가 GitHub에 있다면, 로컬에서 시도한 병합이나 rebase를 버리고 원격 상태로 복원하는 것을 권장합니다.

1. `git status`로 상태를 확인합니다. Rebase가 진행 중이면 `git rebase --abort`로, 병합이 진행 중이면 `git merge --abort`로 취소합니다. 충돌을 해결하며 편집한 파일을 남기려면 취소 전에 따로 복사합니다. [Git rebase 문서](https://git-scm.com/docs/git-rebase) · [Git merge 문서](https://git-scm.com/docs/git-merge)
2. `git branch --show-current`로 현재 브랜치 이름을 확인하고 `git fetch origin`으로 최신 원격 상태를 받습니다.
3. **`git reset --hard`는 미커밋 변경을 버리고, 원격에 올리지 않은 커밋을 현재 브랜치에서 제거합니다.** 남겨야 할 변경은 `git stash push -u`로 보관하고, 로컬 커밋은 `git branch backup/product-search-before-reset`처럼 백업 브랜치로 보관할 수 있습니다. [Git reset 문서](https://git-scm.com/docs/git-reset)

복원 명령은 `git reset --hard origin/<현재 브랜치명>`입니다. 예를 들어 현재 브랜치가 `feat/product-search`이고 같은 이름의 원격 브랜치가 있다면 아래 명령을 실행합니다.

```sh
git reset --hard origin/feat/product-search
```

현재 브랜치가 `develop`이라면 복원 대상은 `origin/develop`입니다. 같은 이름의 원격 브랜치가 없다면 로컬 작업을 보관하고 조현우 팀장에게 연락합니다.

## 6. 도움이 필요할 때

작업 중 오류가 나거나 충돌 해결, rebase, 복원 과정에서 막히면 **반드시 조현우 팀장에게 연락해 주세요.** 현재 브랜치 이름, 실행한 명령, 오류 메시지, `git status` 결과를 함께 알려주면 어디서부터 확인할지 빠르게 파악할 수 있습니다.
