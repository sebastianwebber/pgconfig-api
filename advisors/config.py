# -*- coding: UTF-8 -*-

import tornado.web
import json
from common import util, bytes, ParameterFormat


def config_hard_disk(drive_type, define_doc):
    category = {}
    # Hard Drive Configuration
    category = {}
    category["category"] = "storage_type"
    category["description"] = "Storage Configuration"
    category["parameters"] = list()

    # random_page_cost
    parameter = {}
    parameter["name"] = "random_page_cost"
    parameter["format"] = ParameterFormat.Float

    abstract = "Sets the planner's estimate of the cost of a \
non-sequentially-fetched disk page."
    default_value = "4.0"

    recomendation_posts = {}
    recomendation_posts[
        "How a single PostgreSQL config change improved slow query performance by 50x"] = "https://amplitude.engineering/how-a-single-postgresql-config-change-improved-slow-query-performance-by-50x-85593b8991b0"

    parameter["documentation"] = define_doc(
        parameter["name"],
        "runtime-config-query.html#GUC-RANDOM-PAGE-COST", abstract,
        default_value, recomendation_posts)

    values = {"HDD": 4.0, "SSD": 1.1, "SAN": 1.1}
    parameter["formula"] = values[drive_type]

    category["parameters"].append(parameter)

    # effective_io_concurrency
    parameter = {}
    parameter["name"] = "effective_io_concurrency"
    parameter["format"] = ParameterFormat.Decimal

    abstract = "Sets the number of concurrent disk I/O operations that \
PostgreSQL expects can be executed simultaneously."
    default_value = "1"

    recomendation_posts = {}
    recomendation_posts[
        "PostgreSQL: effective_io_concurrency benchmarked"] = "https://portavita.github.io/2019-07-19-PostgreSQL_effective_io_concurrency_benchmarked/"


    parameter["documentation"] = define_doc(
        parameter["name"],
        "runtime-config-resource.html#GUC-EFFECTIVE-IO-CONCURRENCY",
        abstract, default_value, recomendation_posts)

    values = {"HDD": 2, "SSD": 200, "SAN": 300}
    parameter["formula"] = values[drive_type]

    category["parameters"].append(parameter)

    return category


def config_worker_process(pg_version, cpus, define_doc):
    category = {}

    if cpus < 0:
        return category

    # Worker Processes
    if float(pg_version) >= 9.5:
        category["category"] = "worker_processes"
        category["description"] = "Worker Processes"
        category["parameters"] = list()

        parameter = {}
        parameter["name"] = "max_worker_processes"
        parameter["format"] = ParameterFormat.Decimal

        abstract = "Sets the maximum number of background processes that \
the system can support."
        default_value = 8 if float(pg_version) >= 9.6 else 1

        parameter["documentation"] = define_doc(
            parameter["name"],
            "runtime-config-resource.html#GUC-MAX-WORKER-PROCESSES",
            abstract, default_value)

        parameter["formula"] = cpus
        category["parameters"].append(parameter)

        if float(pg_version) >= 9.6:
            parameter = {}
            parameter["name"] = "max_parallel_workers_per_gather"
            parameter["format"] = ParameterFormat.Decimal

            abstract = "Sets the maximum number of workers that can be \
started by a single Gather node."
            default_value = 2

            parameter["documentation"] = define_doc(
                parameter["name"],
                "runtime-config-resource.html#GUC-MAX-PARALLEL-WORKERS-PER-GATHER",
                abstract, default_value)

            parameter["formula"] = "(CPUS/2)" if cpus > 1 else default_value
            category["parameters"].append(parameter)

        if float(pg_version) >= 10:
            parameter = {}
            parameter["name"] = "max_parallel_workers"
            parameter["format"] = ParameterFormat.Decimal

            abstract = "Sets the maximum number of workers that the system \
can support for parallel queries."
            default_value = 8

            parameter["documentation"] = define_doc(
                parameter["name"],
                "runtime-config-resource.html#GUC-MAX-PARALLEL-WORKERS",
                abstract, default_value)

            parameter["formula"] = cpus
            category["parameters"].append(parameter)

    return category
