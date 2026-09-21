# 문서 로더 (Document Loader) 개념 정리


## 1. 문서 로더란?

문서 로더는 **다양한 형태의 데이터 소스(PDF, 텍스트, CSV, 웹 페이지 등)를 읽어 LangChain이 다룰 수 있는 표준 형식인 `Document` 객체로 변환**해 주는 도구입니다.

RAG(검색 증강 생성) 파이프라인에서는 가장 첫 단계에 해당합니다.

```
문서 로드(Load) → 분할(Split) → 임베딩(Embed) → 벡터 저장소 저장(Store) → 검색(Retrieve) → 생성(Generate)
   ▲ 여기
```

소스의 형식이 무엇이든 로더를 거치고 나면 동일한 `Document` 리스트가 되므로, 이후 단계(분할, 임베딩 등)를 소스와 무관하게 똑같이 처리할 수 있습니다.

## 2. Document 객체

모든 로더의 결과물입니다. 두 가지 필드로 구성됩니다.

| 필드 | 설명 |
|---|---|
| `page_content` | 문서의 본문 텍스트 (`str`) |
| `metadata` | 출처, 페이지 번호, 작성자 등 부가 정보 (`dict`) |

```python
from langchain_core.documents import Document

doc = Document(
    page_content="본문 내용",
    metadata={"source": "manual", "page": 1},
)
```

- 로더 없이 `Document`를 **직접 생성**할 수도 있습니다.
- `metadata`는 나중에 검색 결과의 **출처 표시**, **필터링**에 활용됩니다.

## 3. 공통 사용 패턴

거의 모든 로더가 같은 인터페이스를 가집니다.

```python
loader = SomeLoader(source)   # 1) 로더 생성
docs = loader.load()          # 2) 전체를 한 번에 읽어 list[Document] 반환
```

### `load()` vs `lazy_load()`

| 메서드 | 반환 | 특징 |
|---|---|---|
| `load()` | `list[Document]` | 전체를 한꺼번에 메모리에 올림. 간단하고 편리함 |
| `lazy_load()` | `Iterator[Document]` | 하나씩 읽어 처리. **대용량 파일에서 메모리 절약** |

```python
for doc in loader.lazy_load():
    print(doc.metadata["page"], len(doc.page_content))
```

## 4. 로더 종류별 정리

| 로더 | 대상 | Document 분할 단위 | 추가 설치 |
|---|---|---|---|
| `PyPDFLoader` | PDF | 페이지 1장 = Document 1개 | `pypdf` |
| `PyMuPDFLoader` | PDF | 페이지 1장 = Document 1개 | `pymupdf` |
| `TextLoader` | 텍스트(.txt) | 파일 전체 = Document 1개 | - |
| `CSVLoader` | CSV | **행 1개 = Document 1개** | - |
| `WebBaseLoader` | 웹 페이지 | URL 1개 = Document 1개 | `beautifulsoup4` |
| `DirectoryLoader` | 폴더 내 여러 파일 | 내부 `loader_cls`에 따름 | (내부 로더에 따라) |
| `Docx2txtLoader` | Word(.docx) | 파일 전체 = Document 1개 | `docx2txt` |
| `WikipediaLoader` | 위키피디아 검색 결과 | 문서 1개 = Document 1개 | `wikipedia` |

### 4-1. PDF: `PyPDFLoader`

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("../data/SPRI_AI_Brief_2023년12월호_F.pdf")
docs = loader.load()

print(len(docs))                  # 23 (전체 페이지 수)
print(docs[0].page_content[:300]) # 첫 페이지 본문
print(docs[0].metadata)           # source, page, total_pages, page_label 등
```

- 페이지 단위로 분할되므로 `metadata["page"]`는 **0부터 시작**하고, 사람이 보는 페이지 번호는 `page_label`(1부터)입니다.
- 실습 결과 페이지별 글자 수 편차가 컸습니다. 표지·목차 같은 페이지는 10~17자에 불과한 반면 본문 페이지는 1,000~2,000자였습니다. 그래서 분할·임베딩 전에 너무 짧은 Document를 걸러낼지 고려할 만합니다.

### 4-2. PDF: `PyMuPDFLoader`

```python
from langchain_community.document_loaders import PyMuPDFLoader

docs = PyMuPDFLoader(FILE_PATH).load()
```

- 사용법은 `PyPDFLoader`와 동일합니다.
- 추출 속도가 더 빠르고, 메타데이터(`title`, `author`, `subject`, `keywords`, `format` 등)가 더 풍부합니다.

### 4-3. 텍스트: `TextLoader`

```python
loader = TextLoader("../data/sample.txt", encoding="utf-8")
```

- 한글 파일은 인코딩 오류가 잦으므로 **`encoding="utf-8"`을 명시**하는 것이 안전합니다.

### 4-4. CSV: `CSVLoader`

```python
loader = CSVLoader("../data/sample.csv", encoding="utf-8")
docs = loader.load()  # 행 하나가 Document 하나
```

- 각 행이 `컬럼명: 값` 형태의 텍스트로 변환되어 하나의 Document가 됩니다.

### 4-5. 웹 페이지: `WebBaseLoader`

```python
loader = WebBaseLoader("https://example.com")
docs = loader.load()
```

- HTML을 파싱하기 위해 `beautifulsoup4`가 필요합니다.
- 인터넷 연결이 필요합니다.

### 4-6. 폴더 전체: `DirectoryLoader`

```python
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    "../data",
    glob="**/*.pdf",        # 읽을 파일 패턴 (하위 폴더 포함)
    loader_cls=PyPDFLoader, # 각 파일에 사용할 로더
)
docs = loader.load()
```

- `glob` 패턴에 맞는 파일을 모두 찾아, 파일마다 `loader_cls`로 지정한 로더를 적용합니다.
- 결과는 모든 파일의 Document가 하나의 리스트로 합쳐진 형태입니다.

### 4-7. Word: `Docx2txtLoader`

```python
loader = Docx2txtLoader("../data/sample.docx")
docs = loader.load()
```

- Word 문서는 페이지 구분이 없어 **문서 전체가 Document 하나**로 반환됩니다. `metadata`에는 `source`만 들어갑니다.

### 4-8. 위키피디아: `WikipediaLoader`

```python
loader = WikipediaLoader(query="인공지능", lang="ko", load_max_docs=2)
docs = loader.load()
```

- `query`(검색어), `lang`(언어), `load_max_docs`(가져올 문서 수)를 지정합니다.
- 실습에서는 "인공지능", "생성형 인공지능" 2개 문서가 반환되었고, 각 본문은 4,000자로 잘려 있었습니다. 기본 설정이 문서당 글자 수를 제한하기 때문에, 전체 본문이 필요하면 옵션 확인이 필요합니다.

## 5. 로더 선택 가이드

| 상황 | 추천 |
|---|---|
| 일반적인 PDF | `PyPDFLoader` |
| PDF 속도가 중요하거나 메타데이터가 더 필요 | `PyMuPDFLoader` |
| 폴더에 같은 형식 파일이 여러 개 | `DirectoryLoader` + `loader_cls` |
| 표 형태 데이터를 행 단위로 검색하고 싶음 | `CSVLoader` |
| 온라인 자료 | `WebBaseLoader`, `WikipediaLoader` |
| 지원하는 로더가 없음 | `Document(page_content=..., metadata=...)`로 직접 생성 |

## 6. 주의사항

- **`langchain-community`는 지원 종료(sunset) 예정**입니다. 실습 시 `DeprecationWarning`이 출력되었습니다. 당장은 동작하지만, 장기적으로는 독립 통합 패키지(예: `langchain-pymupdf4llm` 등)로 옮겨 가는 방향입니다.
- **파일 경로**: 노트북의 `../data/sample.*` 경로는 예시이므로 실제 경로에 맞게 수정해야 합니다.
- **추가 패키지**: 로더마다 필요한 패키지가 다릅니다(`pypdf`, `pymupdf`, `beautifulsoup4`, `docx2txt`, `wikipedia`).
- **스캔본 PDF**: 이미지로 된 PDF는 텍스트가 추출되지 않으므로 OCR 기반 로더가 별도로 필요합니다.
- **분할 단위가 곧 검색 단위가 아님**: 로더가 나눈 Document(페이지, 행 등)는 그대로 쓰기에 너무 길거나 짧을 수 있으므로, 보통 다음 단계에서 텍스트 스플리터로 다시 청크 단위로 나눕니다.

## 7. 한 줄 요약

> **문서 로더 = 어떤 형식의 데이터든 `page_content` + `metadata`를 가진 `Document` 리스트로 통일해 주는 RAG의 입구.**
> 사용법은 `Loader(소스).load()` 하나로 공통이며, 소스에 맞는 로더만 고르면 됩니다.
