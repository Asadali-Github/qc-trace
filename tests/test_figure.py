"""The README chart: model names shorten as in the README tables, and the SVG
shows each model's G1 and G3 pass rates."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from run_eval import short_model, svg_figure

def test_short_model_names_match_readme():
    assert short_model("nvidia/nemotron-3-ultra-550b-a55b:free") == "nemotron-3-ultra"
    assert short_model("nvidia/nemotron-3.5-super-vl:free") == "nemotron-3.5-super"
    assert short_model("anthropic/claude-opus-5.5") == "claude-opus-5.5"

def test_svg_figure_shows_both_rates(tmp_path):
    out = tmp_path / "fig.svg"
    svg_figure({"m": {"n": 54, "g1": 54, "g3": 30}}, str(out), "t")
    body = out.read_text(encoding="utf-8")
    assert body.startswith("<svg") and ">100%<" in body and ">56%<" in body
