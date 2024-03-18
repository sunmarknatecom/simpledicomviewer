## Simple Dicom Viewer Project

### 간단한 DICOM 영상 뷰어를 제작해보도록 하겠습니다.

Fig 1. 프로그램 그림
<img src="/Fig1.png"
/>

준비물
1. 미리 설치된 파이썬
2. 파이썬 패키지: pydicom, numpy, pyinstaller

쉘에서 실행 기준
파이썬 패키지 설치
```python
C:\pip install pydicom, numpy, pyinstaller
```

코드를 실행해보고 결과 확인
```python
C:\python simpledicomviewer.py
```

pyinstaller로 랩핑
```python
C:\pyinstaller -w -F simpledicomviewer.py
```

결과는 hiddenimports로 인해 실행되지 않음.
simpledicomviewer.spec 파일을 텍스트편집기에서 열고서
```
hiddenimports=['pydicom.encoders.gdcm', 'pydicom.encoders.pylibjpeg'],
```
수정후
```python
C:\pyinstaller simpledicomviewer.spec
```

완성
