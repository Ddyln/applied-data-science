.PHONY: clean-media video-low video-high

clean-media:
	rm -rf media

video-low:
	manim -ql src/main.py OmniRouter

video-high:
	manim -qh src/main.py OmniRouter