# 작업 흐름: 이슈 → 브랜치 → PR

GitHub Flow를 따른다. `main`은 항상 실행 가능한 상태로 두고, 모든 작업은 이슈에서 시작해 PR로 병합한다.

## 1. 이슈 만들기

| 템플릿 | 언제 | 제목 |
| --- | --- | --- |
| 📅 오늘 할 일 | 하루 단위 학습·실습 작업 | `[W00] 한 줄 요약` |
| 🧪 비교 실험 | A vs B 비교 실험 (1–3일) | `[EXP] 한 줄 요약` |
| 🐛 버그·막힘 | 스크립트 오류, 30분 이상 막힌 문제 | `[BUG] 한 줄 요약` |

이슈 하나는 하루 안에 끝낼 수 있는 크기로 쪼갠다. 학습단위의 완료 기준과 목표는 Notion 🗓️ 단계별 학습 계획을 따른다.

## 2. 브랜치 만들기

```bash
git switch main
git pull
git switch -c feat/12-latency-warmup
```

이름은 `<type>/<이슈번호>-<영문 요약>` 형식이고, type은 커밋 접두어와 같은 네 가지만 쓴다.

| type | 용도 |
| --- | --- |
| `feat` | 새 스크립트·기능, 비교 실험 코드 |
| `fix` | 버그 수정 |
| `docs` | README, 개념 노트, 실험 노트, ADR |
| `chore` | 의존성, 설정, 폴더 정리 |

비교 실험 이슈는 실험 코드가 중심이면 `feat`, 이미 있는 코드로 측정만 하고 실험 노트를 쓰면 `docs` 브랜치로 진행한다.

## 3. 커밋

`CLAUDE.md` 규칙을 따른다: 한국어 메시지, `feat:`·`fix:`·`docs:`·`chore:` 접두어, AI attribution 줄 없음.

## 4. PR과 병합

```bash
git push -u origin feat/12-latency-warmup
gh pr create --fill
```

- PR 본문의 `Closes #12`로 병합할 때 이슈가 자동으로 닫힌다.
- 체크리스트를 확인한 뒤 **Squash and merge**로 병합하고 브랜치를 지운다.
- 병합 후 `git switch main && git pull`로 로컬을 맞춘다.
