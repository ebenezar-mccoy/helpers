nexus = 'http://some.host:8081/nexus/service/local/'

r_mock = [
    # when not exist in any repo
    ['artifact/maven/resolve?r=releases&g=com.cinemacity&a=no-app&p=war&v=RELEASE',
     '<Response [404]>'],
    ['artifact/maven/resolve?r=snapshots&g=com.cinemacity&a=no-app&p=war&v=LATEST',
     '<Response [404]>'],
    ['repositories/rc/content/com/cinemacity/no-app/', '<Response [404]>'],
    # when only snaphost exist
    ['artifact/maven/resolve?r=releases&g=com.cinemacity&a=app-1&p=war&v=RELEASE',
        '<Response [404]>'],
    ['artifact/maven/resolve?r=snapshots&g=com.cinemacity&a=app-1&p=war&v=LATEST',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-1","version":"1.1.1-11111111.1111111-1","baseVersion":"1.1.1-SNAPSHOT","extension":"war","sha1":"a7ba79d8b638f9d6a7e047a509c638eb813f4067"}}'],
    ['repositories/rc/content/com/cinemacity/app-1/', '<Response [404]>'],
    # when only release(master) exist
    ['artifact/maven/resolve?r=releases&g=com.cinemacity&a=app-2&p=war&v=RELEASE',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-2","version":"2.2.2","extension":"jar","sha1":"96703a787c879ecb714667247eb7180760c24260"}}'],
    ['artifact/maven/resolve?r=snapshots&g=com.cinemacity&a=app-2&p=war&v=LATEST',
        '<Response [404]>'],
    ['repositories/rc/content/com/cinemacity/app-2/', '<Response [404]>'],
    # when only rc-hotfix exist
    ['artifact/maven/resolve?r=releases&g=com.cinemacity&a=app-3&p=war&v=RELEASE',
        '<Response [404]>'],
    ['artifact/maven/resolve?r=snapshots&g=com.cinemacity&a=app-3&p=war&v=LATEST',
        '<Response [404]>'],
    ['repositories/rc/content/com/cinemacity/app-3/',
     '{"data":[{"text": "3.3.3.3-SNAPSHOT"}]}'],
    ['artifact/maven/resolve?r=rc&g=com.cinemacity&a=app-3&p=war&v=3.3.3.3-SNAPSHOT',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-3","version":"3.3.3.3-33333333.333333-3","baseVersion":"3.3.3.3-SNAPSHOT","extension":"war","sha1":"a7ba79d8b638f9d6a7e047a509c638eb813f4067"}}'],
    # when only rc-release exist
    ['artifact/maven/resolve?r=releases&g=com.cinemacity&a=app-4&p=war&v=RELEASE',
        '<Response [404]>'],
    ['artifact/maven/resolve?r=snapshots&g=com.cinemacity&a=app-4&p=war&v=LATEST',
        '<Response [404]>'],
    ['repositories/rc/content/com/cinemacity/app-4/',
     '{"data":[{"text": "4.4.4-SNAPSHOT"}]}'],
    ['artifact/maven/resolve?r=rc&g=com.cinemacity&a=app-4&p=war&v=4.4.4-SNAPSHOT',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-4","version":"4.4.4-44444444.444444-4","baseVersion":"4.4.4-SNAPSHOT","extension":"war","sha1":"a7ba79d8b638f9d6a7e047a509c638eb813f4067"}}'],
    # latest rc hotfix/release selector
    ['artifact/maven/resolve?r=releases&g=com.cinemacity&a=app-5&p=war&v=RELEASE',
        '<Response [404]>'],
    ['artifact/maven/resolve?r=snapshots&g=com.cinemacity&a=app-5&p=war&v=LATEST',
        '<Response [404]>'],
    ['repositories/rc/content/com/cinemacity/app-5/',
     '{"data":[{"text": "5.5.1-SNAPSHOT"},{"text": "5.5.2-SNAPSHOT"},{"text": "5.5.5.1-SNAPSHOT"},{"text": "5.5.5.2-SNAPSHOT"}]}'],
    ['artifact/maven/resolve?r=rc&g=com.cinemacity&a=app-5&p=war&v=5.5.2-SNAPSHOT',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-5","version":"5.5.2-5555555.555555-5","baseVersion":"5.5.2-SNAPSHOT","extension":"war","sha1":"a7ba79d8b638f9d6a7e047a509c638eb813f4067"}}'],
    ['artifact/maven/resolve?r=rc&g=com.cinemacity&a=app-5&p=war&v=5.5.5.2-SNAPSHOT',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-5","version":"5.5.5.2-5555555.555555-5","baseVersion":"5.5.5.2-SNAPSHOT","extension":"war","sha1":"a7ba79d8b638f9d6a7e047a509c638eb813f4067"}}'],
    # master newer then rc
    ['artifact/maven/resolve?r=releases&g=com.cinemacity&a=app-6&p=war&v=RELEASE',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-6","version":"6.1.2","extension":"jar","sha1":"96703a787c879ecb714667247eb7180760c24260"}}'],
    ['artifact/maven/resolve?r=snapshots&g=com.cinemacity&a=app-6&p=war&v=LATEST',
     '<Response [404]>'],
    ['repositories/rc/content/com/cinemacity/app-6/',
     '{"data":[{"text": "6.1.1-SNAPSHOT"},{"text": "6.1.1.1-SNAPSHOT"}]}'],
    ['artifact/maven/resolve?r=rc&g=com.cinemacity&a=app-6&p=war&v=6.1.1-SNAPSHOT',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-6","version":"6.1.1-11111111.1111111-1","baseVersion":"6.1.1-SNAPSHOT","extension":"war","sha1":"a7ba79d8b638f9d6a7e047a509c638eb813f4067"}}'],
    ['artifact/maven/resolve?r=rc&g=com.cinemacity&a=app-6&p=war&v=6.1.1.1-SNAPSHOT',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-6","version":"6.1.1.1-11111111.1111111-1","baseVersion":"6.1.1.1-SNAPSHOT","extension":"war","sha1":"a7ba79d8b638f9d6a7e047a509c638eb813f4067"}}'],
    # master older then rc
    ['artifact/maven/resolve?r=releases&g=com.cinemacity&a=app-7&p=war&v=RELEASE',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-7","version":"7.1.1","extension":"jar","sha1":"96703a787c879ecb714667247eb7180760c24260"}}'],
    ['artifact/maven/resolve?r=snapshots&g=com.cinemacity&a=app-7&p=war&v=LATEST',
     '<Response [404]>'],
    ['repositories/rc/content/com/cinemacity/app-7/',
     '{"data":[{"text": "7.1.2-SNAPSHOT"},{"text": "7.1.1.1-SNAPSHOT"}]}'],
    ['artifact/maven/resolve?r=rc&g=com.cinemacity&a=app-7&p=war&v=7.1.2-SNAPSHOT',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-6","version":"7.1.2-11111111.1111111-1","baseVersion":"7.1.2-SNAPSHOT","extension":"war","sha1":"a7ba79d8b638f9d6a7e047a509c638eb813f4067"}}'],
    ['artifact/maven/resolve?r=rc&g=com.cinemacity&a=app-7&p=war&v=7.1.1.1-SNAPSHOT',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-6","version":"7.1.1.1-11111111.1111111-1","baseVersion":"7.1.1.1-SNAPSHOT","extension":"war","sha1":"a7ba79d8b638f9d6a7e047a509c638eb813f4067"}}'],
    # master eq rc RELEASE
    ['artifact/maven/resolve?r=releases&g=com.cinemacity&a=app-8&p=war&v=RELEASE',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-8","version":"8.1.1","extension":"jar","sha1":"96703a787c879ecb714667247eb7180760c24260"}}'],
    ['artifact/maven/resolve?r=snapshots&g=com.cinemacity&a=app-8&p=war&v=LATEST',
     '<Response [404]>'],
    ['repositories/rc/content/com/cinemacity/app-8/',
     '{"data":[{"text": "8.1.1-SNAPSHOT"}]}'],
    ['artifact/maven/resolve?r=rc&g=com.cinemacity&a=app-8&p=war&v=8.1.1-SNAPSHOT',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-8","version":"8.1.1-11111111.1111111-1","baseVersion":"8.1.1-SNAPSHOT","extension":"war","sha1":"a7ba79d8b638f9d6a7e047a509c638eb813f4067"}}'],
    # master eq rc hotfix
    ['artifact/maven/resolve?r=releases&g=com.cinemacity&a=app-9&p=war&v=RELEASE',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-9","version":"9.1.1.1","extension":"jar","sha1":"96703a787c879ecb714667247eb7180760c24260"}}'],
    ['artifact/maven/resolve?r=snapshots&g=com.cinemacity&a=app-9&p=war&v=LATEST',
     '<Response [404]>'],
    ['repositories/rc/content/com/cinemacity/app-9/',
     '{"data":[{"text": "9.1.1.1-SNAPSHOT"}]}'],
    ['artifact/maven/resolve?r=rc&g=com.cinemacity&a=app-9&p=war&v=9.1.1.1-SNAPSHOT',
        '{"data":{"groupId":"com.cinemacity","artifactId":"app-9","version":"9.1.1.1-11111111.1111111-1","baseVersion":"9.1.1.1-SNAPSHOT","extension":"war","sha1":"a7ba79d8b638f9d6a7e047a509c638eb813f4067"}}'],
]
