import kfp
from kfp import dsl
from kubernetes.client import V1Volume, V1VolumeMount, V1HostPathVolumeSource, V1EnvVar, V1ObjectReference


@dsl.pipeline(
    name='vbg pipeline',
    description='vbg pipeline'
)
def ai2_pipeline(cmd: str ='python run_training.py -gpu 0 -experiment_name=grachev-test',
                 GIT_BRANCH: str = 'origin/AI-177-wandb'):
    """A pipeline with two sequential steps."""
    '''ai/pipelines/simple.py'''
    host_volume = V1Volume(name='data-volume', host_path=V1HostPathVolumeSource(path="/data/k8s", type="Directory"))
    host_volume_mount = V1VolumeMount(mount_path='/data', name='data-volume')
    shm_volume = V1Volume(name='shm-volume', host_path=V1HostPathVolumeSource(path="/dev/shm", type="Directory"))
    shm_volume_mount = V1VolumeMount(mount_path='/dev/shm', name='shm-volume')

    dsl.ContainerOp(name='Main', image='cprc/ai:vbg', arguments=[cmd]) \
        .add_node_selector_constraint('kubernetes.io/hostname', 'sjc02-c01-dgx01.stage.ringcentral.com') \
        .add_env_variable(V1EnvVar(name='GIT_BRANCH', value=GIT_BRANCH)) \
        .add_volume(host_volume) \
        .add_volume_mount(host_volume_mount) \
        .add_volume(shm_volume) \
        .add_volume_mount(shm_volume_mount) \
        .set_image_pull_policy("Always")

    dsl.get_pipeline_conf() \
        .set_image_pull_secrets([V1ObjectReference(name="docker-registry")])


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(ai2_pipeline, __file__ + '.yaml')
