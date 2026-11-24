# Picky

AI Agent와 SO-101 로봇팔을 이용한 자연어 기반 pick & place 프로젝트입니다. 웹에서 상품을 요청하면 Gemini Robotics ER 2로 상품을 식별하고, SO-101으로 집어 배출구에 전달하는 서비스를 목표로 합니다.

**팀원은 작업을 시작하기 전에 [Git 협업 가이드](GITGUIDE.md)를 반드시 읽어 주세요.**

현재 실행 범위는 웹 기본 화면, API 상태 확인, Agent 초기화까지입니다. MuJoCo는 Conda 환경에 포함되어 있어 이후 시뮬레이션 개발에 사용할 수 있습니다.

## Conda 설치

Agent, LeRobot, MuJoCo를 PC에서 실행하려면 Conda가 필요합니다. [Miniforge 공식 설치 안내](https://github.com/conda-forge/miniforge#install)에서 운영체제와 CPU에 맞는 설치 파일을 받으세요.

- **macOS**에서는 `.pkg` 설치 파일을 실행한 뒤 새 터미널을 엽니다.
- **Windows**에서는 `.exe` 설치 파일을 실행한 뒤 시작 메뉴에서 **Miniforge Prompt**를 엽니다.
- **Linux**에서는 `.sh` 설치 파일을 `bash`로 실행합니다. 설치 과정에서 셸 초기화를 선택한 뒤 새 터미널을 엽니다.

설치가 끝났거나 Conda가 이미 설치되어 있다면 다음 명령으로 확인합니다.

```sh
conda --version
```

## 저장소와 `picky` 환경 준비

Git이 설치된 터미널에서 저장소를 받습니다.

```sh
git clone --branch develop --recurse-submodules https://github.com/hnuu785/Picky.git
cd Picky
```

이미 `--recurse-submodules` 없이 clone했다면 저장소 루트에서 `git submodule update --init --recursive`를 실행해 LeRobot을 받아옵니다.

저장소 루트에서 `picky` 환경을 만들면 FastAPI, Gemini SDK, MuJoCo, LeRobot이 한 번에 설치됩니다.

```sh
conda env create -f environment.yml
conda activate picky
```

이미 `picky` 환경이 있다면 `conda env update -n picky -f environment.yml`로 의존성을 한 번에 갱신합니다.

## 빠른 시작

웹과 API는 Docker에서 실행됩니다. [Docker Compose](https://docs.docker.com/compose/install/)를 설치하고 Docker를 실행한 뒤, 저장소 루트에서 두 서비스를 함께 시작합니다.

```sh
docker compose up --build --wait
```

- Picky 웹 화면은 <http://localhost:3000>에서 엽니다.
- API 상태는 <http://localhost:3000/api/health>에서 확인합니다. `{"status":"ok"}`가 나오면 웹을 통한 API 연결도 정상입니다.

종료하려면 저장소 루트에서 `docker compose stop`을 실행합니다.

## 구성

| 경로 | 역할 | 실행 환경 |
| --- | --- | --- |
| `picky-fe/` | 웹 화면과 `/api` 요청 전달 | Next.js, Node.js 24, npm |
| `picky-be/` | API 서버 | FastAPI, Python 3.12 |
| `picky-agent/` | Gemini Robotics ER 2 클라이언트 초기화 | Conda `picky` |
| `lerobot/` | SO-101과 카메라 연결 도구 | Git 서브모듈, Conda `picky` |

## Agent와 MuJoCo

저장소 루트에서 MuJoCo 설치를 확인합니다.

```sh
python -c "import mujoco; print(mujoco.__version__)"
```

Agent를 확인하려면 루트에 `.env`가 없는 경우 [.env.example](.env.example)을 `.env`로 복사하고 `GEMINI_API_KEY`를 입력합니다. 키는 로컬 `.env`에 보관합니다.

```sh
python picky-agent/main.py
```

Agent 명령은 클라이언트 초기화 결과를 출력한 뒤 종료합니다.

## 웹·API 소스 수정

Docker Compose를 중지한 다음, 저장소 루트에서 FastAPI 개발 서버를 시작합니다.

```sh
python -m uvicorn main:app --app-dir picky-be --reload --reload-dir picky-be
```

Node.js 24가 설치된 상태에서 다른 터미널을 열고, 저장소 루트에서 Next.js 개발 서버를 시작합니다.

```sh
cd picky-fe
npm ci
npm run dev
```

### SO-101과 카메라 연결

장비를 연결할 PC에서 `picky` 환경을 활성화한 뒤, 저장소 루트에서 LeRobot 로딩을 확인합니다.

```sh
python picky-agent/main.py --robot
```

장비를 연결한 뒤 `lerobot-find-port`로 SO-101 포트를, `lerobot-find-cameras opencv`로 카메라 ID를 확인합니다. 카메라 명령이 저장한 테스트 프레임은 `outputs/`에서 볼 수 있습니다. [LeRobot SO-101 안내](https://huggingface.co/docs/lerobot/so101)

## LAN 배포와 서버 교체

SO-101과 카메라가 연결된 PC 한 대에서 웹과 API를 실행합니다. 서버 PC에서 장비용 Conda 환경을 준비하고, 루트 `.env`에 `PICKY_BIND_HOST=0.0.0.0`을 설정합니다. 방화벽에서 같은 네트워크의 웹 포트 접근을 허용한 뒤 `docker compose up --build --wait`를 실행합니다. 팀원은 `http://<서버-PC의-LAN-IP>:3000`으로 접속합니다. Gemini를 사용할 때는 장비 PC에 인터넷 연결이 필요합니다.

다른 팀원 PC로 서버를 옮길 때는 다음 순서로 진행합니다.

1. 새 PC에 기존 서버와 같은 Git 커밋을 받고 Docker와 Conda `picky`를 준비합니다. 새 PC의 `.env`에 접속 설정과 Gemini 키를 입력합니다.
2. 기존 서버에서 `docker compose stop`을 실행한 뒤 SO-101과 카메라를 새 PC에 연결합니다.
3. 기존 로봇 ID를 그대로 쓴다면 `<robot-id>.json` 보정 파일을 옮깁니다. 현재 LeRobot의 기본 경로는 `~/.cache/huggingface/lerobot/calibration/robots/so_follower/`입니다. 새 PC의 시리얼 포트와 카메라 ID는 다시 확인합니다.
4. 새 PC에서 Compose를 실행하고, 같은 네트워크의 다른 PC에서 웹과 `/api/health`를 확인한 뒤 새 주소를 팀에 공유합니다.
