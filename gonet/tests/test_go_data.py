"""
Tests for code related to GoData.
"""
import os
from unittest.mock import patch, Mock

import numpy as np

from gonet.data import Data


class TestGoData:
    """
    A class for the Data test suite.
    """

    @patch('numpy.random.permutation')
    def test_data_shuffling(self, mock_permutation):
        go_data = Data()
        go_data.images = np.array([1, 2, 3])
        go_data.labels = np.array(['a', 'b', 'c'])
        mock_permutation.return_value = [2, 0, 1]

        go_data.shuffle()

        go_data.images = np.array([3, 1, 2])
        go_data.labels = np.array(['c', 'a', 'b'])

    def test_mat_data_to_numpy_for_images_automatically_uses_the_correct_transpose(self):
        mock_mat_data = Mock()
        mock_get_array = np.empty((10, 20, 3, 300))
        mock_mat_data.get.return_value = mock_get_array.transpose()  # Matlab's hdf5 gives a reverse order.

        array = Data().convert_mat_data_to_numpy_array(mock_mat_data, 'images')

        assert array.shape == (300, 10, 20, 3)

    def test_mat_data_to_numpy_for_depths_automatically_uses_the_correct_transpose(self):
        mock_mat_data = Mock()
        mock_get_array = np.empty((10, 20, 300))
        mock_mat_data.get.return_value = mock_get_array.transpose()  # Matlab's hdf5 gives a reverse order.

        array = Data().convert_mat_data_to_numpy_array(mock_mat_data, 'images')

        assert array.shape == (300, 10, 20)

    def test_mat_data_to_numpy_for_accelerometer_gives_correct_shape(self):
        mock_mat_data = Mock()
        mock_get_array = np.empty((300, 4))
        mock_mat_data.get.return_value = mock_get_array.transpose()  # Matlab's hdf5 gives a reverse order.

        array = Data().convert_mat_data_to_numpy_array(mock_mat_data, 'accelData')

        assert array.shape == (300, 4)

    def test_data_path_property(self):
        go_data = Data()
        go_data.settings.data_directory = 'directory'
        go_data.data_name = 'file_name'

        assert go_data.data_path == os.path.join('directory', 'file_name')

