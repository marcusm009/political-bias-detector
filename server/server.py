from starlette.applications import Starlette
from starlette.responses import UJSONResponse
import gpt_2_simple as gpt2
import tensorflow as tf
import uvicorn
import os
import gc
import sys
import time

app = Starlette(debug=False)

sess = gpt2.start_tf_sess(threads=1)
gpt2.load_gpt2(sess)

# Needed to avoid cross-domain issues
response_header = {
    'Access-Control-Allow-Origin': '*'
}

generate_count = 0


@app.route('/', methods=['GET', 'POST', 'HEAD'])
async def homepage(request):
    global generate_count
    global sess

    if request.method == 'GET':
        params = request.query_params
    elif request.method == 'POST':
        params = await request.json()
    elif request.method == 'HEAD':
        return UJSONResponse({'text': ''},
                             headers=response_header)

    query = "// {} ||".format(params.get('query',''))

    print("Query received: {}".format(params.get('query','')))

    start_time = time.time()

    text = gpt2.generate(sess,
                         length=1,
                         temperature=0.7,
                         top_k=0,
                         top_p=0,
                         prefix=query,
                         return_as_list=True
                         )[0]

    pred_time = time.time() - start_time

    try:
        prediction = text.split(' || ')[1]
    except:
        prediction = "Unsure"

    print("Prediction: {}".format(prediction))
    print("Time elapsed: {:.2f}s".format(pred_time))

    generate_count += 1
    if generate_count == 8:
        # Reload model to prevent Graph/Session from going OOM
        tf.reset_default_graph()
        sess.close()
        sess = gpt2.start_tf_sess(threads=1)
        gpt2.load_gpt2(sess)
        generate_count = 0

    gc.collect()
    return UJSONResponse({'prediction': prediction,
                          'pred_time': '{:.2f}s'.format(pred_time)},
                          headers=response_header)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000

    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

    uvicorn.run(app, host=host, port=int(os.environ.get('PORT', port)))
