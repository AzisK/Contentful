print(
    "__file__={0:<35} | __name__={1:<20} | __package__={2:<20}".format(
        __file__, __name__, str(__package__)
    )
)

import etl_user_events as etl


def test_insert_str():
    tuples = [
        ("A", "B", "C", "123", None, None, "", "2021-01-01"),
        ("X", "Y", "Z", "987", None, None, "", "2001-01-01"),
    ]
    expected_insert_records = """
('A','B','C','123',NULL,NULL,NULL,'2021-01-01'),
('X','Y','Z','987',NULL,NULL,NULL,'2001-01-01')
    """.strip()
    insert_records = etl.UserEventsEtl.insert_str(tuples)
    assert (
        insert_records == expected_insert_records
    ), f"{insert_records} are expected to be {expected_insert_records}"
