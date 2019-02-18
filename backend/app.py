from flask import Flask, jsonify, render_template, send_file

import colors
import configuration
import metadata
import redis_detection
import state

app = Flask(__name__, template_folder='.')
###
### Routes
###

### Adapted from 'Kubernetes in Action' Chapter 6: Volumes: attaching disk storage to containers
@app.route('/api/v1/fortune')
def v1_fortune():
   fortune_file = '/data/fortune/index.html'
   try:
       return send_file(fortune_file)
   except Exception as e:
       return "Could not read fortune file from " + fortune_file + ". Is the volume mounted?"

@app.route('/api/v1/configuration')
def v1_configuration():
    return jsonify({
        'liveness_probe_enabled': configuration.liveness_probe_enabled,
        'readiness_probe_enabled': configuration.readiness_probe_enabled,
        'redis_host': configuration.redis_host,
        'state': configuration.state,
        'version': configuration.version,
        'description': configuration.description,
    })

@app.route('/api/v1/metadata')
def v1_metadata():
    return jsonify({
        'hostname': metadata.hostname,
        'node': metadata.node,
        'pod': metadata.pod,
        'namespace': metadata.namespace,
        'ip': metadata.ip,
        'description': metadata.description,
    })

@app.route('/api/v1/state')
def v1_state():
    image_link, state_hits = state.state_function()
    return jsonify({
        'type': configuration.state,
        'image_link': image_link,
        'state_hits': state_hits,
    })

@app.route('/api/v1/redis_detection')
def v1_redis_detection():
    return jsonify({
        'is_detected': redis_detection.is_detected,
        'description': redis_detection.description,
    })

@app.route('/api/v1/colors')
def v1_colors():
    return jsonify(colors.deterministic_colors)

### Liveness Probe
if configuration.liveness_probe_enabled:
    @app.route('/probe/liveness')
    def liveness_probe():
        return 'I am doing well!'

### Readiness Probe
if configuration.readiness_probe_enabled:
    @app.route('/probe/readiness')
    def readiness_probe():
        # TODO: Add dependency checks on database
        return 'I am doing well!'


app.run(host='0.0.0.0', port=8080, debug=True)
print('Hello, this is backend!')  # So we can see it in the `kubectl` logs.
