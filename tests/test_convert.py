import urllib.request

from .utils import cmd, converted_process, runserver


TEST_APP = "scale"
TEST_SCRIPT = f"examples/{TEST_APP}.py"
TEST_BIND = "127.0.0.1:8042"
TEST_HTTP = f"http://{TEST_BIND}/"
TIMEOUT = 10


def test_runserver__fbv_with_model(tmp_path):
    cmd(TEST_SCRIPT, "run", "makemigrations", TEST_APP)
    cmd(TEST_SCRIPT, "run", "migrate")
    cmd(TEST_SCRIPT, "convert", str(tmp_path), "--name=converted", "--delete")

    with (
        converted_process(tmp_path, "runserver", TEST_BIND) as handle,
        runserver(handle),
    ):
        response = urllib.request.urlopen(TEST_HTTP, timeout=TIMEOUT)
        assert response.getcode() == 200
        assert "Number of page loads" in response.read().decode("utf-8")
