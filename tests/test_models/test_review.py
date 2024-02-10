#!/usr/bin/python3
import unittest
import datetime
from models.review import Review
from models import storage
from models.base_model import BaseModel


class TestAmenity(unittest.TestCase):
    def test_initialization_no_kwargs(self):
        review = Review()
        self.assertIsInstance(review, Review)
        self.assertEqual(review.place_id, "")

        review = Review()
        review.place_id = "Amenity"
        self.assertEqual(review.place_id, "Amenity")

    def test_attribute_value(self):
        review = Review()

        review.place_id = "New name"
        self.assertEqual(review.place_id, "New name")

    def test_string_representation(self):
        # Test the __str__ method
        review = Review()
        review.place_id = "New Amen"
        expected_str = "[Review] ({}) {}".format(review.id, review.__dict__)
        self.assertEqual(str(review), expected_str)

    def test_save_method(self):
        # Test the save method
        review = Review()
        original_updated_at = review.updated_at
        review.save()
        self.assertNotEqual(review.updated_at, original_updated_at)

    def test_to_dict_method(self):
        # Test the to_dict method
        review = Review()
        review.place_id = "New Amen"
        review_dict = review.to_dict()
        self.assertIsInstance(review_dict, dict)
        self.assertIn('__class__', review_dict)
        self.assertIn('id', review_dict)
        self.assertIn('created_at', review_dict)
        self.assertIn('updated_at', review_dict)
        self.assertEqual(review_dict['place_id'], "New Amen")

    def test_storage_interaction(self):
        # Test interaction with storage
        review = Review()
        review.place_id = "New Amen"
        review.save()
        self.assertIn(
            f"{review.__class__.__name__}.{review.id}", storage.all())

    def test_inheritance(self):
        # Test inheritance from BaseModel
        review = Review()
        self.assertIsInstance(review, Review)
        self.assertIsInstance(review, BaseModel)

if __name__ == "__main__":
    unittest.main()
