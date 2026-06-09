from drug_intelligence import PROJECT_NAME, RESEARCH_ONLY_NOTICE, __version__


def test_package_metadata_is_present() -> None:
    assert PROJECT_NAME == "Drug Intelligence"
    assert __version__ == "0.1.0"


def test_research_only_notice_is_explicit() -> None:
    notice = RESEARCH_ONLY_NOTICE.lower()
    assert "research prototype" in notice
    assert "not medical advice" in notice
    assert "not clinical decision support" in notice
