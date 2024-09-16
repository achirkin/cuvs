# Copyright (c) 2024, NVIDIA CORPORATION.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

header = """/*
 * Copyright (c) 2024, NVIDIA CORPORATION.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/*
 * NOTE: this file is generated by q_search_single_cta_00_generate.py
 *
 * Make changes there and run in this directory:
 *
 * > python q_search_single_cta_00_generate.py
 *
 */

#include "search_single_cta_inst.cuh"
#include "compute_distance_vpq.cuh"

namespace cuvs::neighbors::cagra::detail::single_cta_search {
"""

trailer = """
}  // namespace cuvs::neighbors::cagra::detail::single_cta_search
"""

# block = [(64, 16), (128, 8), (256, 4), (512, 2), (1024, 1)]
# itopk_candidates = [64, 128, 256]
# itopk_size = [64, 128, 256, 512]
# mxelem = [64, 128, 256]

pq_bits = [8]
subspace_dims = [2, 4]

# rblock = [(256, 4), (512, 2), (1024, 1)]
# rcandidates = [32]
# rsize = [256, 512]
code_book_types = ["half"]

search_types = dict(
    float_uint32=("float", "uint32_t", "float"),  # data_t, idx_t, distance_t
    half_uint32=("half", "uint32_t", "float"),
    int8_uint32=("int8_t", "uint32_t", "float"),
    uint8_uint32=("uint8_t", "uint32_t", "float"),
    float_uint64=("float", "uint64_t", "float"),
    half_uint64=("half", "uint64_t", "float"),
)

# knn
for type_path, (data_t, idx_t, distance_t) in search_types.items():
    for code_book_t in code_book_types:
        for subspace_dim in subspace_dims:
            for pq_bit in pq_bits:
                path = f"q_search_single_cta_{type_path}_{pq_bit}pq_{subspace_dim}subd_{code_book_t}.cu"
                with open(path, "w") as f:
                    f.write(header)
                    f.write(
                            f"instantiate_kernel_selection(\n  cuvs::neighbors::cagra::detail::cagra_q_dataset_descriptor_t<{data_t} COMMA {code_book_t} COMMA {pq_bit} COMMA {subspace_dim} COMMA {distance_t} COMMA {idx_t}>, cuvs::neighbors::filtering::none_cagra_sample_filter);\n"
                    )

                    f.write(trailer)
                    # For pasting into CMakeLists.txt
                    print(f"src/neighbors/detail/cagra/{path}")
