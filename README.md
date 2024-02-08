# Interview assignment

### Prerequisites:

- Python 3.11 or higher
- sqlite

### Steps:

1. **Create virtual env**

   ```
   python -m venv venv
   ```

2. **Activate virtual environment**

    ```
    source /venv/bin/activate.fish
    ```
4. **Install Dependencies**

    ```
    pip install -r requirements.txt
    
    ```

4. **Run:**

    ```
    python app.py
    ```

### Configuration:

Repository contains `config.py` file with predefined configuration setup.

By default `DEBUG` mode is enabled causing logging SQL queries as well as cache info.

!! Warning, since the size of chunks read from the csv is quite big, the processing time is smaller than 5 sec that were assumed for refreshing data in database. !!

Therefore, in order to see the cache stats, either provide bigger file or decrease the size of a chunks in `app.py`.


### Final words to provided solution:

I used iterator and chunks during reading the csv file with pandas library, to prevent loading whole file in the memory, which could lead to OOM. 

While getting chunk from iterator, I used vectorized function and chained the operation on DataFrame to gain speed advantage and saved some memory. 

To limit roundtrips to database, I implemented custom `lru_cache` wrappper that allows to set a TTL.

I thought about using Spark for this project however, since it's a coding assignment and Spark would handle most of the stuff for me I decided to do everything on my own. 

In real world scenario, I would definitely reach for field proven solutions that can scale easily and provide great interface for all calculations needed for this assignment.

Lastly, to improve performance of my solution, I would try leverage numpy lib and it's C level implementation to hit L1 cache. SIMD would also be beneficial here, but I would have to figure out how to vectorize some of the operations. 


