# A wrapper around pip package to pull in undeclared dependencies.

load("@requirements//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

licenses(["restricted"])  # GPL

py_library(
    name = "libxmp",
    srcs = ["libxmp.py"],
    deps = [
        requirement("python-xmp-toolkit"),
        requirement("pytz"),
    ],
)
